import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

PRIME1 = 4801
PRIME2 = 3461

SUM = PRIME1 + PRIME2
DIFF = PRIME1 - PRIME2

SUM_BYTES = SUM.to_bytes(2, byteorder="little")
DIFF_BYTES = DIFF.to_bytes(2, byteorder="little")

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("92hHBfhRXkQe2zNwu7eYowNu32Wv2CcQmw7ZTas2GUqjSh51PUG")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index):
    txout_scriptPubKey = [OP_2DUP, OP_SUB, OP_HASH160, Hash160(DIFF_BYTES), OP_EQUALVERIFY, OP_ADD, OP_HASH160, Hash160(SUM_BYTES), OP_EQUAL]
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, [txout], txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)
    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.009
    txid_to_spend = ('fe6858c54284164c68c2945269325fad368fc5b4463c3f9ddb69551254fad4be')
    utxo_index = 0
    print("Address = ", my_address)
    print("Public_key = ", my_public_key.hex())
    print("Private_key = ", my_private_key.hex())
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index)
    print(response.status_code, response.reason)
    print(response.text)
