import bitcoin.wallet
from bitcoin.core import b2lx
from utils import *
import time,struct
import hashlib

bitcoin.SelectParams('mainnet')
my_public_key = bitcoin.wallet.CBitcoinSecret('5K3pc5RJ688SrsimfqWr7BJn5irtXMsVmkkZYWpc9Vk8tCz3yBS').pub
print('Address = ',bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key))
COINBASE_HEX_DATA = '810199457NesaAbbasi'.encode('utf-8').hex()
print('coinbase hexadecimal data: ', COINBASE_HEX_DATA)
BLOCK_REWARD = 6.25

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def get_target(bits):
    exponent = bits[2:4]
    coefficient = bits[4:]
    target = int(coefficient, 16) * (int("2" , 16) ** (8 * (int(exponent,16) - 3)))
    target_hex = format(target, 'x')
    target_byte = bytes.fromhex(str(target_hex).zfill(64))
    print("Target in hex: ", str(target_hex).zfill(64))
    return target_byte

def make_coinbase_transaction(amount_to_send):
    txid_to_spend = (64*'0')
    utxo_index = int('0xffffffff', 16)
    txout_scriptPubKey = P2PKH_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    new_tx = CMutableTransaction([txin], [txout])
    txin.scriptSig =  CScript([int(COINBASE_HEX_DATA, 16).to_bytes(len(COINBASE_HEX_DATA)//2, 'big')])
    return new_tx

def get_merkle_root(coinbase_tx):
    merkle_root = b2lx(hashlib.sha256(hashlib.sha256(coinbase_tx.serialize()).digest()).digest())
    print("Merkle root: ", merkle_root)
    block_body = (coinbase_tx.serialize()).hex()
    print("Block body: ", block_body)
    return merkle_root, block_body

def get_partial_header(version, prev_hash_block, merkle_root, timestamp, bits):
    partial_header = struct.pack('<L', version) + bytes.fromhex(prev_hash_block)[::-1] + bytes.fromhex(merkle_root)[::-1] + struct.pack('<LL', timestamp, int(bits, 16))
    return partial_header

def block_mining(prev_block_hash, bits):
    coinbase_tx = make_coinbase_transaction(BLOCK_REWARD)
    merkle_root, block_body = get_merkle_root(coinbase_tx)
    partial_header = get_partial_header(2, prev_block_hash, merkle_root, int(time.time()), bits)
    nonce = 0
    target = get_target(bits)
    while nonce <= 0xFFFFFFFF: # = 2**32 
        header = partial_header + struct.pack('<L', nonce)
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        start_time = time.time()
        if hash[::-1] < target:
            print('Hash: ', hash)
            print('Nonce: ', nonce)
            print('Hash rate: ', nonce/(time.time() - start_time))
            return hash, header, block_body
        nonce += 1

def main():
    n = input("please enter your block number: ")
    # n = 9457
    prev_block_hash = input("please enter prevoius block hash: ")
    # prev_block_hash = '00000000d5dde2b1403c05b8546073aaab6b1c599fa86cf32751dc32d027e712'
    bits = '0x1f010000'   
    hash, header, block_body = block_mining(prev_block_hash, bits)
    print("Block hash:", b2lx(hash))
    print("Block header:", header.hex())
    block_size = len(header) + len(b'\x01') + len(block_body)
    magic_number = 0xD9B4BEF9.to_bytes(4, "little")
    block_body = bytes.fromhex(block_body)
    print("Block: ", magic_number + struct.pack("<L", block_size) + header + b'\x01' + block_body)


if __name__ == '__main__':
    main()