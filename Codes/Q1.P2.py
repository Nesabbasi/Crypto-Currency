import hashlib
import secrets
import ecdsa
import base58

TESTNET_PRIVATE = b'\xef'
TESTNET_PUBLIC = b'\x6f'

def make_private_key():
    private_key = secrets.token_bytes(32)
    return private_key

def wif(key, prefix):
    new_key = prefix + key
    base58_checking = base58.b58encode_check(new_key)
    return base58_checking


def make_public_key(private_key):
    public_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key
    return public_key

def pay_to_public_key_hash(public_key):
    hash_byte = hashlib.sha256(public_key).digest()
    new_hash = hashlib.new( "ripemd160", hash_byte).digest()
    return new_hash, wif(new_hash, TESTNET_PUBLIC)

def vanity_address(start_chars):
    while True:
        private_key = make_private_key()
        final_private_key = wif(private_key, TESTNET_PRIVATE)
        public_key = make_public_key(private_key)
        hash, final_public_key = pay_to_public_key_hash(b'\04' + public_key.to_string())
        if final_public_key[1:4] == start_chars:
            print(hash)
            return final_public_key, final_private_key, public_key, private_key
        
final_public_key, final_private_key, public_key, private_key = vanity_address(b'nes')

print(f'''Private_key WIF = {final_private_key} \nPublic key P2PKH= {final_public_key}''')
print(f'''Private_key = {private_key} \nPublic key = {public_key.to_string()}''')