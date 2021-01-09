# # AES 256 encryption/decryption using pycrypto library
#
# import base64
# import hashlib
# from Crypto.Cipher import AES
# from Crypto import Random
#
# BLOCK_SIZE = 16
# pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
#     BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]
#
# password = input("Enter encryption password: ")
#
#
# def encrypt(raw, password):
#     private_key = hashlib.sha256(password.encode("utf-8")).digest()
#     raw = pad(raw)
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(private_key, AES.MODE_CBC, iv)
#     encrypted = base64.b64encode(iv + cipher.encrypt(raw))
#     return str(encrypted, 'utf-8')
#
#
# def decrypt(enc, password):
#     private_key = hashlib.sha256(password.encode("utf-8")).digest()
#     enc = base64.b64decode(enc)
#     iv = enc[:16]
#     cipher = AES.new(private_key, AES.MODE_CBC, iv)
#     return unpad(cipher.decrypt(enc[16:]))
#
#
# # First let us encrypt secret message
# encrypted = encrypt("This is a secret message", password)
# print(encrypted)
#
# # Let us decrypt using our original password
# decrypted = decrypt(encrypted, password)
# print(bytes.decode(decrypted))


# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import os
import pickle
import codecs


# pad with spaces at the end of the text
# beacuse AES needs 16 byte blocks
def pad(s):
    block_size = 16
    remainder = len(s) % block_size
    padding_needed = block_size - remainder
    return s + padding_needed * b'0'


# remove the extra spaces at the end
def unpad(s):
    return s.rstrip()


def encrypt(plain_text, password):
    # generate a random salt
    salt = os.urandom(AES.block_size)

    # generate a random iv
    #iv = Random.new().read(AES.block_size)
    iv = 'This is an IV456'.encode()

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8,
                                 p=1, dklen=32)

    # pad text with spaces to be valid for AES CBC mode
    padded_text = pad(plain_text)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_CBC, iv)

    # return a dictionary with the encrypted text
    return {
        'cipher_text': base64.b64encode(cipher_config.encrypt(padded_text)),
        'salt': base64.b64encode(salt),
        'iv': base64.b64encode(iv)
    }


def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = base64.b64decode(enc_dict['salt'])
    enc = base64.b64decode(enc_dict['cipher_text'])
    iv = base64.b64decode(enc_dict['iv'])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8,
                                 p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_CBC, iv)

    # decrypt the cipher text
    decrypted = cipher.decrypt(enc)

    # unpad the text to remove the added spaces
    original = unpad(decrypted)

    return original
import chardet
def split_to_chunks(file):
    CHUNK_SIZE = 10000
    list_of_chunks = []
    with open(file, 'rb') as f:
    # with codecs.open(file, 'rb', 'utf-16') as f:

        while True:
            data = f.read(CHUNK_SIZE)
            print('THE ENDOGING', str(chardet.detect(data)))
            list_of_chunks.append(data)
            if not data:
                break
    return list_of_chunks

def build_file(list_of_chunks, dec_file):
    # with open(dec_file, 'wb') as f:
    with codecs.open(dec_file, 'wb', 'utf-16') as f:
        for c in list_of_chunks:
            #decoded = (c.decode('utf-8')).decode('utf-8')
            print('c: ', c)
            print('decode: ', c.decode('utf-8'))
            print('str-decode: ', str(c, 'utf-8'))
            # decode = str(c, 'utf-8')
            # print(type(decode))

            #decoded = c.decode('utf-8')

            #print(str(decoded, 'utf-8'))
            #print('in decoded', decoded.decode("utf-8"))

            f.write(c)
    print('[+] File wrote')

def encrypt_using_chunks(dec_file, enc_file, password):
    chunks = split_to_chunks(dec_file)
    encrypted_chunks = []
    for c in chunks:
        # print('encrypt_using_chunks c: ',c)
        #print('encrypt_using_chunks c decoded: ', c.decode('utf-8'))
        encrypted_chunks.append(encrypt(c, password))
    with open(enc_file, 'wb') as f:
        pickle.dump(encrypted_chunks, f)

def decrypt_using_chunks(enc_file, dec_file, password):
    decrypted_chunks = []
    with open(enc_file, 'rb') as f:
        encrypted_chunks = pickle.load(f)
        for c in encrypted_chunks:
            print('test')
            decrypted_chunks.append(decrypt(c, password))

            print(len(decrypted_chunks))

        build_file(decrypted_chunks, dec_file)

def main():

    file_encrypted = '/home/michal/garbage/logo.jpeg.enc'
    file_decrypted = '/home/michal/garbage/logo_dec.jpeg'

    file2 = '/home/michal/garbage/logo.jpeg'
    file2_encrypted = '/home/michal/garbage/logo.jpeg.enc'
    file2_decrypted = '/home/michal/garbage/logo_dec.jpeg'

    file3 = '/home/michal/garbage/test.txt'
    file3_encrypted = '/home/michal/garbage/test.txt.enc'
    file3_decrypted = '/home/michal/garbage/test_dec.txt'

    # encrypt_using_chunks(file3, file3_encrypted, 'haslo')
    # decrypt_using_chunks(file3_encrypted, file3_decrypted, 'haslo')
    # os.system('md5sum ' + file3)
    # os.system('md5sum ' + file3_decrypted)

    encrypt_using_chunks(file2, file2_encrypted, 'haslo')
    decrypt_using_chunks(file2_encrypted, file2_decrypted, 'haslo')
    os.system('md5sum ' + file2)
    os.system('md5sum ' + file2_decrypted)

main()