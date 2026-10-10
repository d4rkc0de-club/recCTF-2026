
import time
from web3 import Web3

RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
WALLET = Web3.to_checksum_address(
    "0xCBc82A20b93dd7dA5302f0cc584e8B645983beea"
)
FIRST_TX_HASH = (
    "0x2625c3dd50c8ba82376978ce008262e8bbd11fd2f35879a23726971c96ebffae"
)

POSITIONS = [
    40, 62, 84, 116, 132, 166, 259, 264, 322, 353,
    366, 424, 460, 475, 532, 553, 575, 595, 612, 628,
    694, 770, 811, 862, 902, 930, 937, 978, 993
]

w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 30}))

if not w3.is_connected() or w3.eth.chain_id != 11155111:
    raise RuntimeError("Sepolia RPC connection failed")

first = w3.eth.get_transaction(FIRST_TX_HASH)

if first["from"].lower() != WALLET.lower():
    raise RuntimeError("First transaction sender does not match wallet")

START_NONCE = first["nonce"]
START_BLOCK = first["blockNumber"]

targets = {START_NONCE + p: p for p in POSITIONS}
found = {}

print(f"[+] Starting nonce: {START_NONCE}")
print(f"[+] Starting block: {START_BLOCK}")
print(f"[+] Target nonces: {sorted(targets)}")

block_num = START_BLOCK

while len(found) < len(POSITIONS):
    try:
        latest = w3.eth.block_number

        while block_num <= latest and len(found) < len(POSITIONS):
            block = w3.eth.get_block(block_num, full_transactions=True)

            for tx in block["transactions"]:
                if tx["from"].lower() != WALLET.lower():
                    continue

                nonce = tx["nonce"]
                if nonce not in targets:
                    continue

                position = targets[nonce]
                data = bytes(tx["input"])

                print(
                    f"\n[MATCH] block={block_num} nonce={nonce} "
                    f"position={position} data={data.hex() or '(empty)'}"
                )

                # Original format: one raw byte per flag transaction.
                if len(data) == 1:
                    found[position] = data[0]
                    print(f"[FLAG BYTE] {position}: {chr(data[0])!r}")
                else:
                    print("[!] Input is not a single byte; inspect data above.")

            block_num += 1

        if len(found) == len(POSITIONS):
            break

        print(
            f"[WAIT] Scanned through block {block_num - 1}; "
            f"recovered {len(found)}/{len(POSITIONS)}"
        )
        time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopped.")
        break
    except Exception as exc:
        print(f"[ERROR] {exc}")
        time.sleep(3)

print("\nFinished.")