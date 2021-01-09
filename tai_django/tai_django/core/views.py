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
import pickle
import mimetypes


class Home(TemplateView):
    template_name = 'home.html'

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
            # encrypted_list.append(encrypted)
    # for chunk in in_file.chunks():
    #     padded_data = pad_message(chunk)
    #     encrypted = cipher.encrypt(padded_data)
    #     encrypted_list.append(encrypted)
    #
    # with open(out_file, 'wb') as f:
    #     pickle.dump(encrypted_list, f)



def decrypt_file(in_file, out_file, password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    CHUNK_SIZE = 8000
    # with open(in_file, 'rb') as f:
    #     to_decrypt = pickle.load(f)
    # with open(out_file, 'wb') as f2:
    #     for c in to_decrypt:
    #         decrypted_part = cipher.decrypt(c)
    #         f2.write(decrypted_part.rstrip(b'0'))
    with open(out_file, 'wb') as f2:
        with open(in_file,'rb') as f:
            while True:
                to_decrypt = f.read(CHUNK_SIZE)
                plain_text = cipher.decrypt(to_decrypt)
                f2.write(plain_text.rstrip(b'0'))
                if not to_decrypt:
                    break

def process_chunk(chunk):
    # print('[*] Chunk processing...')
    # chunk = str(chunk, 'utf-8')
    password = 'haslo'.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 'This is an IV456'
    cipher = AES.new(key, mode, IV)
    plain_text = cipher.decrypt(chunk)
    chunk = plain_text.rstrip(b'0')
    return chunk
    # return chunk

def download(request):
    path = '/home/michal/PycharmProjects/TAI/tai_django/media/'

    if request.method == 'GET':
        f = request.GET.get('f')
        if f:
            chunk_size = 8000
            file_path = path + str(f)
            print(file_path)
            response = StreamingHttpResponse(
                (process_chunk(chunk)
                for chunk in FileWrapper(open(file_path,'rb'),chunk_size)),
                content_type="application/octet-stream")
            # response['Content-Length'] = os.path.getsize(file_path)
            # response[
            #     'Content-Disposition'] = "attachment; filename=%s" % f
            return response
        else:
            print('No parameters')
            print('Not downloading files')
        file_list = os.listdir(path)
        print(file_list)
        return render(request,'download.html', {'files': file_list})
    # return render(request, 'download.html')


# def download_decrypt(request, in_file, out_file, password):
#     file_path = '/home/michal/PycharmProjects/TAI/tai_django/media/out.enc'
#     chunk_size = 8000
#     filename = os.path.basename(file_path)
#     response = StreamingHttpResponse(
#         ( chunk_processing(chunk)
#           for chunk in FileWrapper(open(file_path,'rb'),chunk_size),
#         content_type="application/octet-stream")
#     response['Content-Length'] = os.path.getsize(file_path)
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     return response



def handle_uploaded_file(f):
    with open('/home/michal/PycharmProjects/TAI/tai_django/media/33_mb.bin',
              'wb+') as \
            destination:
        for chunk in f.chunks():
            print('chunks')
            destination.write(chunk)

def upload(request):
    if request.method == 'POST':
        encrypt_file(request.FILES['document'],
                      '/home/michal/PycharmProjects/TAI/tai_django/media/out'
                      '.enc', 'haslo')
        # print('test')
        # decrypt_file('/home/michal/PycharmProjects/TAI/tai_django/media/out'
        #              '.enc',
        #              '/home/michal/PycharmProjects/TAI/tai_django/media/out'
        #              '.dec', 'haslo')
        #
        # print(os.system('md5sum '+'/home/michal/PycharmProjects/TAI/tai_django'
        #                    '/media/logo.jpeg'))
        # print(os.system('md5sum '+
        #           '/home/michal/PycharmProjects/TAI/tai_django/media/out.dec'))






        # print(file_size)
        # fh = FileUploadHandler()
        # fh.new_file(uploaded_file, uploaded_file.name, content_type=content_type,
        #             content_length=content_length, charset=charset)
        # test1 = fh.receive_data_chunk(uploaded_file, 2000)
        # print('test')


        #fs = FileSystemStorage()
        #fs.save(uploaded_file.name, uploaded_file)
        #print(uploaded_file.name)
        #print(uploaded_file.size)
    return render(request, 'upload.html')



# def download(request):
#    the_file = '/some/file/name.png'
#    filename = os.path.basename(the_file)
#    chunk_size = 8192
#    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
#                            content_type=mimetypes.guess_type(the_file)[0])
#    response['Content-Length'] = os.path.getsize(the_file)
#    response['Content-Disposition'] = "attachment; filename=%s" % filename
#    return response