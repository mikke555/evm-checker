# EVM Balance Checker

Balance checker for Ethereum and EVM. Uses async and multicall for efficiency and displays results in a user-friendly format.

Proxy usage is recommended.


## Features ✨
- Checks multiple addresses simultaneously
- Batches balance calls into a single RPC request
- Supports any EVM chain with a multicall contract deployed
- Supports ERC-20 tokens
- Shows USD values via Binance API
- Proxy support for rate limiting
- CSV export
  
## Installation 🚀

1. **Clone the repository**
```bash
git clone https://github.com/mikke555/evm-checker.git
cd evm-checker
```

2. **Setup virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup files**
- Add wallet addresses to `addresses.txt` (one per line)
- *(Optional)* Add HTTP proxies to `proxies.txt` (format: `username:password@ip:port`)

## Usage 🎯

```bash
python main.py
```

Select your chain from the interactive menu. Results are displayed in a table and saved to `results/` as CSV.

## File Structure 📁

- `main.py` - Main script
- `config.py` - Chain configurations and token contracts
- `addresses.txt` - Wallet addresses to check
- `proxies.txt` - HTTP proxies (optional)
- `abi/` - Contract ABI files
- `results/` - Output CSV files

