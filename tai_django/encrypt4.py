from Crypto.Cipher import AES
import hashlib
import os

def pad_message(file):
    while len(file)% 16 != 0:
        file = file + b'0'
    return file

def encrypt(message):
    password = 'mypassword'.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'

    cipher = AES.new(key, mode, IV)
    padded_msg = pad_message(message)
    encrypted_msg = cipher.encrypt(padded_msg)
    return encrypted_msg

def decrypt(message):
    password = 'mypassword'.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    decrypted_text = cipher.decrypt(message)
    return decrypted_text

def encrypt_file(file, file2):
    password = 'mypassword'.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    with open(file, 'rb') as f:
        orig_file = f.read()
    padded_file = pad_message(orig_file)
    encrypted_file = cipher.encrypt(padded_file)

    with open(file2, 'wb') as f:
        f.write(encrypted_file)

def decrypt_file(file, file2):
    password = 'mypassword'.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)

    with open(file, 'rb') as f:
        encrypted_file = f.read()
    decrypted_file = cipher.decrypt(encrypted_file)
    with open(file2, 'wb') as f2:
        f2.write(decrypted_file.rstrip(b'0'))

file2 = '/home/michal/garbage/logo.jpeg'
file2_encrypted = '/home/michal/garbage/logo.jpeg.enc'
file2_decrypted = '/home/michal/garbage/logo_dec.jpeg'

file3 = '/home/michal/garbage/test.txt'
file3_encrypted = '/home/michal/garbage/test.txt.enc'
file3_decrypted = '/home/michal/garbage/test_dec.txt'

# encrypt_file(file2, file2_encrypted)
# decrypt_file(file2_encrypted, file2_decrypted)
# os.system('md5sum ' + file2)
# os.system('md5sum ' + file2_decrypted)

encrypt_file(file3, file3_encrypted)
decrypt_file(file3_encrypted, file3_decrypted)
os.system('md5sum ' + file3)
os.system('md5sum ' + file3_decrypted)


