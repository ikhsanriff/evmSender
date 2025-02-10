import random
import time
from web3 import Web3
from eth_utils import is_address

# ANSI escape codes for colors
GREEN = "\033[92m"
RESET = "\033[0m"

# Get user inputs
PRIVATE_KEY = input("Enter your private key: ").strip()
RPC_URL = input("Enter RPC URL: ").strip()
TRANSACTION_COUNT = int(input("Enter the number of transactions to perform: ").strip())

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
SENDER_ADDRESS = w3.eth.account.from_key(PRIVATE_KEY).address if PRIVATE_KEY else None

# Function to check balance
def check_balance(address):
    balance = w3.eth.get_balance(address)
    return w3.from_wei(balance, "ether")

# Function to generate a valid random address
def generate_random_address():
    while True:
        address = "0x" + "".join(random.choices("0123456789abcdef", k=40))
        if is_address(address):
            return w3.to_checksum_address(address)

# Function to send ETH
def send_eth(receiver, amount_eth):
    if not PRIVATE_KEY or not SENDER_ADDRESS:
        print("Private key not found!")
        return None

    nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)
    tx = {
        'nonce': nonce,
        'to': w3.to_checksum_address(receiver),
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'chainId': w3.eth.chain_id  # Dynamic Chain ID
    }
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

# Function to wait for transaction confirmation
def wait_for_transaction_confirmation(tx_hash):
    print(f"Waiting for confirmation of transaction: {tx_hash}")
    confirmations = 0
    while confirmations < 2:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt and receipt.status == 1:
                confirmations = w3.eth.block_number - receipt.blockNumber
                if confirmations >= 2:
                    print(f"{GREEN}Transaction confirmed!{RESET}")
                    break
        except Exception:
            print("Transaction not found yet. Retrying...")
        time.sleep(5)  # Check every 5 seconds

# Example usage
if __name__ == "__main__":
    print(f"Sender balance ({SENDER_ADDRESS}): {check_balance(SENDER_ADDRESS)} ETH")

    for _ in range(TRANSACTION_COUNT):
        random_address = generate_random_address()
        print(f"Sending 0.00001 ETH to: {random_address}")
        tx_hash = send_eth(random_address, 0.00001)
        if tx_hash:
            print(f"{GREEN}Transaction successful! Hash: {tx_hash}{RESET}")
            wait_for_transaction_confirmation(tx_hash)

        # Random delay between transactions to avoid spam
        delay = random.randint(15, 45)  # Delay between 15-45 seconds
        print(f"Waiting {delay} seconds before next transaction...")
        time.sleep(delay)
