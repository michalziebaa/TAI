from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadhandler import MemoryFileUploadHandler
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import UploadedFile
import os

from django.http import StreamingHttpResponse
# from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
from django.http import FileResponse
from django.conf import settings

import base64
from Crypto.Cipher import AES
import hashlib
import os
import time
import pickle
import mimetypes

#global variables
CHUNK_SIZE = 16000
encrypted_upload_path = \
    '/home/dev/PycharmProjects/TAI/tai_django/media/encrypted/'
unencrypted_upload_path = \
    '/home/dev/PycharmProjects/TAI/tai_django/media/unencrypted/'

class Home(TemplateView):
    template_name = 'home.html'


def write_unenc_upload_logs(output):
    with open('unenc_upload.log', 'a') as f:
        f.write("\n"+output)
        f.write('-----------')

def write_unenc_download_logs(output):
    with open('unenc_download.log', 'a') as f:
        f.write("\n"+output)
        f.write('-----------')

def write_enc_upload_logs(output):
    with open('enc_upload.log', 'a') as f:
        f.write("\n"+output)
        f.write('-----------')

def write_enc_download_logs(output):
    with open('enc_download.log', 'a') as f:
        f.write("\n"+output)
        f.write('-----------')

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def pad_message(file):
    while len(file)% 16 != 0:
        file = file + b'0'
    return file

def upload_without_encryption(in_file, out_file):

    encrypted_list = []
    size = in_file.size
    test = in_file.multiple_chunks(chunk_size=1)
    with open(out_file, 'wb') as f2:
        for chunk in in_file.chunks(chunk_size=CHUNK_SIZE):
            f2.write(chunk)
            if not chunk:
                break

def encrypt_file(in_file, out_file, password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)

    encrypted_list = []
    size = in_file.size
    test = in_file.multiple_chunks(chunk_size=1)
    with open(out_file, 'wb') as f2:
        for chunk in in_file.chunks(chunk_size=CHUNK_SIZE):
            data = chunk
            padded_data = pad_message(data)
            encrypted = cipher.encrypt(padded_data)
            f2.write(encrypted)
            if not chunk:
                break


def decrypt_file(in_file, out_file, password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)

    with open(out_file, 'wb') as f2:
        with open(in_file,'rb') as f:
            while True:
                to_decrypt = f.read(CHUNK_SIZE)
                plain_text = cipher.decrypt(to_decrypt)
                f2.write(plain_text.rstrip(b'0'))
                if not to_decrypt:
                    break

def process_chunk(chunk, passwd):
    password = passwd.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    plain_text = cipher.decrypt(chunk)
    chunk1 = plain_text.rstrip(b'0')
    return chunk1

def process_chunk_not_enc(chunk):
    return chunk
    # return chunk

def download(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'enc':
            time_start = time.perf_counter()

            print('proceed encryption')
            file_name = request.POST.get('file_name')
            password = request.POST.get('password')

            file_path = encrypted_upload_path + file_name
            response = StreamingHttpResponse(
                (process_chunk(chunk, password)
                 for chunk in FileWrapper(open(file_path, 'rb'), CHUNK_SIZE))
                , content_type="application/octet-stream")

            file_size = os.stat(file_path).st_size
            time_stop = time.perf_counter()
            download_time = time_stop - time_start
            log = "File size: {}\nDownload time:{}\n".format(file_size,
                                                           download_time)
            write_enc_download_logs(log)
            print("Encrypted Download time: {}".format(download_time))
            return response
            # return response
        else:
            time_start = time.perf_counter()
            print('proceed not encrypted')
            file_name = request.POST.get('file_name')

            file_path = unencrypted_upload_path + file_name
            response = StreamingHttpResponse(
                (process_chunk_not_enc(chunk)
                 for chunk in FileWrapper(open(file_path, 'rb'), CHUNK_SIZE))
                , content_type="application/octet-stream")

            file_size = os.stat(file_path).st_size
            time_stop = time.perf_counter()
            download_time = time_stop - time_start
            log = "File size: {}\nDownload time:{}\n".format(file_size,
                                                           download_time)
            write_unenc_download_logs(log)
            print("NOT encrypted download time: {}".format(download_time))
            return response


    enc_file_list = os.listdir(encrypted_upload_path)
    unenc_file_list = os.listdir(unencrypted_upload_path)

    return render(request,'download.html', {'encfiles': enc_file_list,
                                            'unencfiles': unenc_file_list})


def upload(request):
    if request.method == 'POST':
        file_size = request.FILES['document'].size
        if request.POST["password"]:
            #encrypting file
            time_start = time.perf_counter()
            encrypt_file(request.FILES['document'],
                          encrypted_upload_path+request.FILES[
                             'document'].name+".enc",
                         request.POST[
                             "password"])
            time_stop = time.perf_counter()
            upload_time = time_stop - time_start
            log = "File size: {}\nUpload time:{}\n".format(file_size,
                                                           upload_time)
            write_enc_upload_logs(log)
            print("Encrypted upload time: {}".format(upload_time))

        else:
            #upload withoud encryption
            time_start = time.perf_counter()
            upload_without_encryption(request.FILES['document'],
                          unencrypted_upload_path+request.FILES[
                                          'document'].name)
            time_stop = time.perf_counter()
            upload_time = time_stop - time_start
            log = "File size: {}\nUpload time: {}\n".format(file_size,
                                                               upload_time)
            write_unenc_upload_logs(log)

            print("NOT encrypted upload time: {}".format(upload_time))
        print('File size {}'.format(file_size))

    return render(request, 'upload.html')
