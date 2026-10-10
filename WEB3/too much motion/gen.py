import os
import time
import random
from web3 import Web3

RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
NUM_TXS = 1000
FLAG = b"d4rk{w3b3_1s_0verrat3d_r1ght}"
SEED = 4137

w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 30}))

if not w3.is_connected():
    raise RuntimeError("Sepolia RPC connection failed")

account = w3.eth.account.from_key(os.environ["SEPOLIA_PRIVATE_KEY"])

if w3.eth.chain_id != 11155111:
    raise RuntimeError("Connected network is not Sepolia")

# Place flag bytes at reproducible, shuffled transaction positions.
rng = random.Random(SEED)
positions = sorted(rng.sample(range(NUM_TXS), len(FLAG)))
payloads = {pos: bytes([char]) for pos, char in zip(positions, FLAG)}

# Use the current network gas price.
gas_price = w3.eth.gas_price
nonce = w3.eth.get_transaction_count(account.address, "pending")

# Exact intrinsic gas for a simple legacy transaction with calldata.
def intrinsic_gas(data):
    return 21000 + sum(4 if b == 0 else 16 for b in data)

print("Address:", account.address)
print("Transactions:", NUM_TXS)
print("Gas price:", w3.from_wei(gas_price, "gwei"), "gwei")
print("Flag-byte positions:", positions)

# Save the position list for the challenge author.
with open("flag_positions.txt", "w") as f:
    f.write("\n".join(map(str, positions)))

for i in range(NUM_TXS):
    data = payloads.get(i, b"")

    tx = {
        "chainId": 11155111,
        "nonce": nonce,
        "to": account.address,
        "value": 0,
        "data": data,
        "gas": intrinsic_gas(data),
        "gasPrice": gas_price,
    }

    signed = account.sign_transaction(tx)

    try:
        tx_hash = w3.eth.send_raw_transaction(
            signed.raw_transaction
        )
        print(f"{i + 1}/{NUM_TXS}: {tx_hash.hex()}")
        nonce += 1

    except Exception as e:
        print(f"Submission failed at index {i}: {e}")
        print("Stop here; inspect the pending nonce before retrying.")
        break

    # Avoid overwhelming a public RPC endpoint.
    time.sleep(0.2)

print("Submission loop finished.")
