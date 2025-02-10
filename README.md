# EVM Sender

A simple script to send ETH to random addresses on an EVM-compatible network.

## Features
- Sends ETH to randomly generated valid addresses.
- Waits for 2 confirmations before proceeding to the next transaction.
- Introduces a randomized delay between transactions to avoid spamming.
- Uses Web3.py for blockchain interactions.

## Installation

### Prerequisites
- Python 3.8+
- `pip` package manager

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/ikhsanriff/evmSender.git
   cd evmSender
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Configuration
When running the script, you will be prompted to enter:
- Your private key (ensure it's secure and not exposed).
- An RPC URL (e.g., from Infura, Alchemy, or public RPC nodes).
- The number of transactions to execute.

## Security Warning ⚠️
- **Never share your private key!**
- Consider using environment variables or `.env` files instead of directly inputting your private key.
- Ensure you're on a testnet before using real funds.

## License
This project is licensed under the MIT License.

