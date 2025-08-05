"""
To add new custom chain:
    Get a free public RPC endpoint from https://chainlist.org/
    Alternatively, sign up for https://www.alchemy.com/, https://blastapi.io/, https://www.quicknode.com/ etc.

    Add token contracts if needed.

    Find multicall address for your chain on https://www.multicall3.com/deployments or try with the default one.
"""

DEFAULT_MULTICALL = "0xcA11bde05977b3631167028862bE2a173976CA11"

config = {
    "ethereum": {
        "rpc": ["https://eth-mainnet.public.blastapi.io", "https://1rpc.io/eth", "https://eth.llamarpc.com"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    # Layer2 chains
    "base": {
        "rpc": ["https://mainnet.base.org", "https://1rpc.io/base", "https://base.llamarpc.com"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "OpenUSDT": "0x1217BfE6c773EEC6cc4A38b5Dc45B92292B6E189",
            "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "USDT": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
            "USDT0": "0x102d758f688a4c1c5a80b116bd945d4455460282",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "op": {
        "rpc": ["https://mainnet.optimism.io", "https://optimism-mainnet.public.blastapi.io"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "OpenUSDT": "0x1217BfE6c773EEC6cc4A38b5Dc45B92292B6E189",
            "USDC": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
            "USDC.e": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
            "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
            "USDT0": "0x01bFF41798a0BcF287b996046Ca68b395DbC1071",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "arbitrum": {
        "rpc": ["https://arb1.arbitrum.io/rpc", "https://arbitrum.drpc.org"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
            "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "USDC.e": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
            "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "linea": {
        "rpc": ["https://rpc.linea.build", "https://1rpc.io/linea"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
            "USDC": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
            "USDT": "0xA219439258ca9da29E9Cc4cE5596924745e12B93",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "soneium": {
        "rpc": ["https://soneium-mainnet.public.blastapi.io", "https://soneium.drpc.org"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "OpenUSDT": "0x1217BfE6c773EEC6cc4A38b5Dc45B92292B6E189",
            "USDC.e": "0xbA9986D2381edf1DA03B0B9c1f8b00dc4AacC369",
            "USDT": "0x3A337a6adA9d885b6Ad95ec48F9b75f197b5AE35",
            "USDT0": "0x102d758f688a4C1C5a80b116bD945d4455460282",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "unichain": {
        "rpc": ["https://mainnet.unichain.org", "https://unichain-mainnet.public.blastapi.io"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "OpenUSDT": "0x1217bfe6c773eec6cc4a38b5dc45b92292b6e189",
            "USDC": "0x078d782b760474a361dda0af3839290b0ef57ad6",
            "USDT": "0x588ce4f028d8e7b53b687865d6a67b3a54c75518",
            "USDT0": "0x9151434b16b9763660705744891fa906f660ecc5",
            "UNI": "0x8f187aa05619a017077f5308904739877ce9ea21",
            "DAI": "0x20cab320a855b39f724131c69424240519573f81",
            "WBTC": "0x927b51f251480a681271180da4de28d44ec4afb8",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "ink": {
        "rpc": ["https://rpc-gel.inkonchain.com"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "USDC.e": "0xF1815bd50389c46847f0Bda824eC8da914045D14",
            "USDT0": "0x0200C29006150606B650577BBE7B6248F58470c1",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "lisk": {
        "rpc": ["https://rpc.api.lisk.com"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "OpenUSDT": "0xF1815bd50389c46847f0Bda824eC8da914045D14",
            "USDT": "0x05d032ac25d322df992303dca074ee7392c117b9",
            "USDT0": "0x43F2376D5D03553aE72F4A8093bbe9de4336EB08",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "mode": {
        "rpc": ["https://mainnet.mode.network"],
        "symbol": "ETH",
        "tokens": {
            "WETH": "0x4200000000000000000000000000000000000006",
            "USDC": "0xd988097fb8612cc24eec14542bc03424c656005f",
            "OpenUSDT": "0x1217bfe6c773eec6cc4a38b5dc45b92292b6e189",
            "USDT": "0xf0f161fda2712db8b566946122a5af183995e2ed",
            "USDT0": "0x43F2376D5D03553aE72F4A8093bbe9de4336EB08",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "abstract": {
        "rpc": ["https://api.mainnet.abs.xyz"],
        "symbol": "ETH",
        "tokens": {},
        "multicall": "0xF9cda624FBC7e059355ce98a31693d299FACd963",
    },
    # Other EVM
    "bsc": {
        "rpc": ["https://binance.llamarpc.com"],
        "symbol": "BNB",
        "tokens": {
            "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            "USDT": "0x55d398326f99059ff775485246999027b3197955",
            "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "opbnb": {
        "rpc": ["https://1rpc.io/opbnb"],
        "symbol": "BNB",
        "tokens": {},
        "multicall": DEFAULT_MULTICALL,
    },
    "avax": {
        "rpc": ["https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc"],
        "symbol": "AVAX",
        "tokens": {
            "WAVAX": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
            "BTC.b": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
            "USDC": "0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e",
            "USDT": "0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "polygon": {
        "rpc": ["https://polygon-rpc.com"],
        "symbol": "POL",
        "tokens": {
            "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
            "USDC.e": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
            "USDC": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "USDT": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
        },
        "multicall": DEFAULT_MULTICALL,
    },
    "fantom": {
        "rpc": ["https://fantom-pokt.nodies.app"],
        "symbol": "FTM",
        "tokens": {},
        "multicall": DEFAULT_MULTICALL,
    },
    # Testnets
    "sepolia": {
        "rpc": ["https://0xrpc.io/sep"],
        "symbol": "ETH",
        "tokens": {},
        "multicall": DEFAULT_MULTICALL,
    },
    "monad": {
        "rpc": ["https://testnet-rpc.monad.xyz"],
        "symbol": "MON",
        "tokens": {},
        "multicall": DEFAULT_MULTICALL,
    },
}


import json

with open("abi/multicall.json", "r") as file:
    MULTICALL_ABI = json.load(file)

with open("abi/erc20.json", "r") as file:
    ERC20_ABI = json.load(file)
