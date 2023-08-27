import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("92grWQktDAe6G7NUmJpR6vK1yYRCALkbZ7AaLTQbg2YQtWsTKJk")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

private_key1 = bitcoin.wallet.CBitcoinSecret("92zTJQyVy4QQ1Rv6LFXZVeCcZehhKCBFhpatQZxFgv6X975FFUs")
private_key2 = bitcoin.wallet.CBitcoinSecret("925aN2mT1y2roU6soRAkNYP143vnJFy9UfSsxY4SAcBeb7rVfgK")
private_key3 = bitcoin.wallet.CBitcoinSecret("91wEoys8V76G1SwJKWmzgwu3o8bWkrfeSXJLjutTJmAMGD3vYSN")
public_key1 = private_key1.pub
public_key2 = private_key2.pub
public_key3 = private_key3.pub

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index):
    txout_scriptPubKey = [OP_2, public_key1, public_key2, public_key3, OP_3, OP_CHECKMULTISIG]
    txin_scriptPubKey = P2PKH_scriptPubKey()
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, [txout], txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)
    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.0134
    txid_to_spend = ('d77417d41bd3efdc2e286fd6b15d969ef7ee81802b608993b0b5f585c5618258')
    utxo_index = 0
    print("Address = ", my_address)
    print("Public_key = ", my_public_key.hex())
    print("Private_key = ", my_private_key.hex())
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index)
    print(response.status_code, response.reason)
    print(response.text)