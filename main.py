import asyncio
import csv
import os
import random
import time
from datetime import datetime
from decimal import Decimal

import aiohttp
import questionary
from rich import box
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID
from rich.table import Table
from web3 import AsyncHTTPProvider, AsyncWeb3

from config import ERC20_ABI, MULTICALL_ABI, config

# Constants
console = Console()
MIN_VALUE_TO_DISPLAY = 0.00001
RETRY = 3

# Global state
SELECTED_CHAIN = None
NATIVE_TOKEN = None
TOTAL_ETH = 0


def read_file(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def select_chain() -> None:
    global SELECTED_CHAIN, NATIVE_TOKEN

    chain = questionary.autocomplete(
        "Select chain (type to search):", choices=list(config.keys()), match_middle=False
    ).ask()
    if chain is None:
        exit()
    try:
        SELECTED_CHAIN = chain.lower()
        NATIVE_TOKEN = config[SELECTED_CHAIN]["symbol"]

    except KeyError:
        console.print(f"[yellow]Chain {chain} not found[/yellow]")
        exit()


def get_web3(proxies: list[str]) -> AsyncWeb3:
    assert SELECTED_CHAIN is not None

    rpc_url = random.choice(config[SELECTED_CHAIN]["rpc"])
    kwargs = {"proxy": f"http://{random.choice(proxies)}"} if proxies else {}
    return AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=kwargs))


async def get_token_price() -> Decimal:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={NATIVE_TOKEN}USDT"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return Decimal(data["price"])

    console.print(f"[yellow]Error fetching {NATIVE_TOKEN} price[/yellow]: {response.reason}")
    return Decimal(0)


async def get_balance_from_multicall(address: str, proxies: list[str]) -> dict:
    assert SELECTED_CHAIN is not None

    checksum_address = AsyncWeb3.to_checksum_address(address)
    multicall_address = AsyncWeb3.to_checksum_address(config[SELECTED_CHAIN]["multicall"])
    token_list = list(config[SELECTED_CHAIN]["tokens"].items())

    # Initialize default token balances
    default_token_balances = {token_name: 0 for token_name, _ in token_list}

    for attempt in range(RETRY):
        try:
            web3 = get_web3(proxies)
            multicall = web3.eth.contract(multicall_address, abi=MULTICALL_ABI)
            calls = []

            # Encode eth balance call
            eth_balance_call = multicall.encodeABI("getEthBalance", [checksum_address])
            calls.append({"target": multicall_address, "allowFailure": False, "callData": eth_balance_call})

            # Encode token balance calls
            for token_name, token_address in token_list:
                token_address = web3.to_checksum_address(token_address)
                token_contract = web3.eth.contract(token_address, abi=ERC20_ABI)

                balance_call = token_contract.encodeABI("balanceOf", [checksum_address])
                calls.append({"target": token_address, "allowFailure": False, "callData": balance_call})

                decimals_call = token_contract.encodeABI("decimals", [])
                calls.append({"target": token_address, "allowFailure": False, "callData": decimals_call})

            results = await multicall.functions.aggregate3(calls).call()

            # Parse results
            balance_wei = web3.to_int(results[0][1])
            balance_eth = web3.from_wei(balance_wei, "ether")

            token_balances = {}
            for i, (token_name, token_address) in enumerate(token_list):
                balance_result = results[1 + i * 2]
                decimals_result = results[1 + i * 2 + 1]

                balance = web3.to_int(balance_result[1])
                decimals = web3.to_int(decimals_result[1])

                token_balances[token_name] = float(Decimal(balance) / Decimal(10**decimals))

            # Add small delay before nonce call to avoid 429 error
            await asyncio.sleep(random.uniform(0.05, 0.15))
            nonce = await web3.eth.get_transaction_count(checksum_address)

            return {"address": address, NATIVE_TOKEN: float(balance_eth), **token_balances, "tx_count": int(nonce)}

        except Exception as e:
            if (
                "429" in str(e)
                or "Too Many Requests" in str(e).lower()
                or "call rate limit exhausted" in str(e).lower()
            ):
                # console.print(f"Rate limit hit, retrying in {0.5 * (2 ** attempt)} sec\t{address}")
                await asyncio.sleep(0.5 * (2**attempt))
                continue

    # If all retries failed, return defaults with consistent keys
    console.print(f"[red]Failed to get balance for[/red] {address}")
    return {"address": address, NATIVE_TOKEN: 0.0, **default_token_balances, "tx_count": int(0)}


async def check_balances(
    addresses: list[str], proxies: list[str], progress: Progress, task_id: TaskID, max_concurrent: int = 20
) -> list[dict]:
    if not proxies:
        max_concurrent = 3

    semaphore = asyncio.Semaphore(max_concurrent)
    completed = 0

    async def throttled_get_balance(address: str) -> dict:
        nonlocal completed
        async with semaphore:
            result = await get_balance_from_multicall(address, proxies)
            completed += 1
            progress.update(task_id, completed=completed)
            return result

    tasks = [throttled_get_balance(address) for address in addresses]
    results = await asyncio.gather(*tasks)
    return results


def format_value(value: str | float | int) -> str | int:
    if value == 0:
        return ""
    if isinstance(value, float) and 0 < value < MIN_VALUE_TO_DISPLAY:
        return "~ 0"
    if isinstance(value, float):
        return f"{value:.8f}"
    return value


def print_table(results: list[dict], token_price: Decimal) -> None:
    global TOTAL_ETH

    table = Table(box=box.ASCII_DOUBLE_HEAD, show_footer=True)

    # Add headers and calculate totals
    headers = list(results[0].keys())
    TOTAL_ETH += sum(entry[NATIVE_TOKEN] for entry in results if isinstance(entry[NATIVE_TOKEN], (int, float)))

    for header in headers:
        footer_text = ""
        if header == "address":
            footer_text = "TOTAL"
        elif header == NATIVE_TOKEN:
            footer_text = f"{TOTAL_ETH:.6f}"
        elif header == "USD" and token_price:
            total_usd = Decimal(str(TOTAL_ETH)) * token_price
            footer_text = f"{total_usd:.2f}"

        table.add_column(
            header, footer=footer_text, justify="right" if header != "address" else "left", footer_style="bold green"
        )

    # Add rows
    for result in results:
        formatted_values = [f"[cyan]{format_value(value)}[/cyan]" for value in result.values()]
        table.add_row(*formatted_values)

    console.print(table)


def write_to_csv(results: list[dict], filename: str) -> None:
    headers = list(results[0].keys())
    formatted_values = [{key: str(format_value(value)) for key, value in entry.items()} for entry in results]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(formatted_values)


async def main() -> None:
    assert SELECTED_CHAIN is not None

    addresses = read_file("addresses.txt")
    proxies = read_file("proxies.txt")

    os.makedirs("results", exist_ok=True)
    filename = f"results/{SELECTED_CHAIN}-{datetime.now():%d_%m_%Y_%H_%M_%S}.csv"

    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Checking [cyan]{len(addresses)}[/cyan] addresses on {SELECTED_CHAIN.title()} ",
            total=len(addresses),
        )

        start_time = time.time()
        results = await check_balances(addresses, proxies, progress=progress, task_id=task)
        token_price = await get_token_price()

        if token_price:
            for result in results:
                result["USD"] = float(Decimal(str(result[NATIVE_TOKEN])) * token_price)

    print_table(results, token_price)
    write_to_csv(results, filename)

    console.print(f"\nExecution time: {time.time() - start_time:.2f} seconds")
    console.print(f"Results saved to [green]{filename}[/green]\n")


if __name__ == "__main__":
    try:
        select_chain()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
