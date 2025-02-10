import random
import json
import os
from web3 import Web3
from eth_utils import is_address

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

# Example usage
if __name__ == "__main__":
    print(f"Sender balance ({SENDER_ADDRESS}): {check_balance(SENDER_ADDRESS)} ETH")

    for _ in range(TRANSACTION_COUNT):
        random_address = generate_random_address()
        print(f"Sending 0.00001 ETH to: {random_address}")
        tx_hash = send_eth(random_address, 0.00001)
        if tx_hash:
            print(f"Transaction successful! Hash: {tx_hash}")
