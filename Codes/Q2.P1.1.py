import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91gpQs5JtC2XdHEL7WDGjMeyWgmrCJMEZxY7kKYkaGY6LXE1Mw3")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout1, txout2, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, [txout1, txout2], txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def P2PKH_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def send_from_P2PKH_transaction(amount_to_send1, amount_to_send2, txid_to_spend, utxo_index):
    txout1_scriptPubKey = [OP_TRUE]
    txout2_scriptPubKey = [OP_FALSE]
    txout1 = create_txout(amount_to_send1, txout1_scriptPubKey)
    txout2 = create_txout(amount_to_send2, txout2_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout1, txout2, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, [txout1, txout2], txin_scriptPubKey, txin_scriptSig)
    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send1 = 0.0194
    amount_to_send2 = 0.00000001
    txid_to_spend = ('9f86b5ffa54cb218780b58fdf1fc981fe97b0b95b3e55663b39844874dc55d4b')
    utxo_index = 1
    print("Address = ", my_address)
    print("Public_key = ", my_public_key.hex())
    print("Private_key = ", my_private_key.hex())
    response = send_from_P2PKH_transaction(amount_to_send1, amount_to_send2, txid_to_spend, utxo_index)
    print(response.status_code, response.reason)
    print(response.text) 