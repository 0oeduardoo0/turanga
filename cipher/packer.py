# -*- coding: utf-8 -*-

import hashlib
from lxml import etree
from . import algorithm 

INVALID_FILE_ERR = 0
INVALID_KEY_ERR = 1

def pack(file_name, file_data, key):

   hashed = hashlib.md5(file_name).hexdigest()

   # These 3 bytes indicates that this file is Turanga's encryption
   data  = '<?xml version="1.0"?>\n'
   data += '<trg version="2.1">\n'

   data += '\t<vkey>'
   # Encode a known piece of data to the decoder be able to verify the key
   data += algorithm.encode('_ALL_OK_', key)
   data += '</vkey>\n'

   data += '\t<name>'
   # encode the original file name
   data += algorithm.encode(file_name, key)
   data += '</name>\n'

   data += '\t<data>'
   data += algorithm.encode(file_data, key)
   data += '</data>\n'

   data += '</trg>'

   return hashed, data


def unpack(source, key):

   parser = etree.XMLParser(recover=True)

#   try:
   root = etree.fromstring(source, parser=parser)
#   except:
#      return False, INVALID_FILE_ERR, None, None

   if root.tag != "trg":
      return False, INVALID_FILE_ERR, None, None

   for element in root:
      if element.tag == "vkey":
         verify_key = element.text
      elif element.tag == "name":
         file_name = element.text
      elif element.tag == "data":
         content = element.text

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