# -*- coding: utf-8 -*-

import hashlib
from . import algorithm

INVALID_FILE_ERR = 0
INVALID_KEY_ERR = 1

def pack(file, source, key):

   hashed = hashlib.md5(file).hexdigest()

   # These 3 bytes indicates that this file is Turanga's encryption
   data  = 'trg.'
   # Encode a known piece of data to the decoder be able to verify the key
   data += algorithm.encode('_ALL_OK_', key) + '.'
   # encode the original file name
   data += algorithm.encode(file, key) + '.'

   data += algorithm.encode(source, key)

   return hashed, data


def unpack(source, key):

   # checking the first 3 bytes to know the type of file, 
   # to know if it is a Turanga's encryption
   if not source[0:3] == 'trg':
      return False, INVALID_FILE_ERR, None, None

   trg, verify_key, file_name, content = source.split('.')

   try:
      verify_key = algorithm.decode(verify_key, key)

   except:
      return False, INVALID_KEY_ERR, None, None

   # check These verification key
   if not verify_key == "_ALL_OK_":
      return False, INVALID_KEY_ERR, None, None
   

   file_name = algorithm.decode(file_name, key)
   content = algorithm.decode(content.strip(), key)

   return True, None, file_name, content