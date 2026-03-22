from web3 import Web3
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Monad Testnet config
RPC_URL = "https://rpc.ankr.com/monad_testnet"
CHAIN_ID = 10143
w3 = Web3(Web3.HTTPProvider(RPC_URL))

private_key = os.getenv("PRIVATE_KEY")
if not private_key:
    print("❌ Set PRIVATE_KEY in .env")
    exit(1)

account = w3.eth.account.from_key(private_key)
print(f"✅ Agent running as: {account.address}")

# Check balance
balance_wei = w3.eth.get_balance(account.address)
balance_mon = w3.from_wei(balance_wei, "ether")
print(f"Balance: {balance_mon:.4f} MON")

# Condition: "price dip" mocked by balance threshold (upgrade to real oracle later)
THRESHOLD_MON = 0.1
SWAP_AMOUNT = 0.1

if balance_mon > THRESHOLD_MON:
    # Auto-swap action: send 0.1 MON (demo privacy move — replace with real DEX call later)
    demo_destination = w3.to_checksum_address("0x000000000000000000000000000000000000dead")  # burn address
    
    nonce = w3.eth.get_transaction_count(account.address)
    tx = {
        "nonce": nonce,
        "to": demo_destination,
        "value": w3.to_wei(SWAP_AMOUNT, "ether"),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": CHAIN_ID,
    }
    
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"🚀 SWAP EXECUTED — 0.1 MON moved!")
    print(f"Tx: https://testnet.monadvision.com/tx/{tx_hash.hex()}")
else:
    print("⏸️ No action — balance below threshold (mock dip not triggered)")

print("Agent cycle complete.")

