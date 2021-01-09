from Crypto.Cipher import AES
import hashlib
import os
import pickle

def pad_message(file):
    while len(file)% 16 != 0:
        file = file + b'0'
    return file

def encrypt_file(in_file, out_file, password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    CHUNK_SIZE = 8000
    encrypted_list = []
    with open(out_file, 'wb') as f2:
        with open(in_file, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                padded_data = pad_message(data)
                encrypted = cipher.encrypt(padded_data)
                f2.write(encrypted)
                # encrypted_list.append(encrypted)
                if not data:
                    break
        # with open(out_file, 'wb') as f:
        #     pickle.dump(encrypted_list, f)


def decrypt_file(in_file, out_file, password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    CHUNK_SIZE = 8000
    with open(out_file, 'wb') as f2:
        with open(in_file,'rb') as f:
            while True:
                to_decrypt = f.read(CHUNK_SIZE)
                plain_text = cipher.decrypt(to_decrypt)
                f2.write(plain_text.rstrip(b'0'))
                if not to_decrypt:
                    break
    # with open(in_file, 'rb') as f:
    #     to_decrypt = pickle.load(f)
    # with open(out_file, 'wb') as f2:
    #     for c in to_decrypt:
    #         decrypted_part = cipher.decrypt(c)
    #         f2.write(decrypted_part.rstrip(b'0'))

file2 = '/home/michal/garbage/test_2/sample.txt'
file2_encrypted = '/home/michal/garbage/logo.jpeg.enc'
file2_decrypted = '/home/michal/garbage/test_2/sample_dex.txt'
file2_enc = '/home/michal/garbage/test_2/out.enc'

#encrypt_file(file2, file2_encrypted, 'haslo')
decrypt_file(file2_enc, file2_decrypted, 'haslo')
os.system('md5sum ' + file2)
os.system('md5sum ' + file2_decrypted)



# def split_to_chunks(file):
#     CHUNK_SIZE = 10000
#     list_of_chunks = []
#     with open(file, 'rb') as f:
#     # with codecs.open(file, 'rb', 'utf-16') as f:
#
#         while True:
#             data = f.read(CHUNK_SIZE)
#             print('THE ENDOGING', str(chardet.detect(data)))
#             list_of_chunks.append(data)
#             if not data:
#                 break
#     return list_of_chunks

# def encrypt_using_chunks(dec_file, enc_file, password):
#     chunks = split_to_chunks(dec_file)
#     encrypted_chunks = []
#     for c in chunks:
#         # print('encrypt_using_chunks c: ',c)
#         #print('encrypt_using_chunks c decoded: ', c.decode('utf-8'))
#         encrypted_chunks.append(encrypt(c, password))
#     with open(enc_file, 'wb') as f:
#         pickle.dump(encrypted_chunks, f)