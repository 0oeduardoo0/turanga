# -*- coding: utf-8 -*-
from hashlib import sha256

"""
      encode(data, key)

      Algorithm to encode the source

      @param string data : source for encode
      @param string key  :  key to encode

      @return string
"""
def encode(data, key):

  # first obtain a hash for the key
  # by this way we have a long key
  key = sha256(key).hexdigest()
   
  keysize = len(key)
  key_index = 0
  output = ''

  for character in data:
    if key_index >= keysize:
      key_index = 0
         
    result = (ord(character) + ord(key[key_index])) % 256
         
    output += chr(result)
         
    key_index += 1

  return output.encode("base64").replace("\n","")

"""
      encode(data, key)

      Algorithm to decode the source

      @param string data : source for decode
      @param string key  :  key to decode

      @return string
"""     
def decode(data, key):

  data = data.decode("base64")

  # we need get the hash
  key = sha256(key).hexdigest()
  
  txtsize = len(data)
  keysize = len(key)
  key_index = 0
  output = ''

  count = 0

  for character in data:
    if key_index >= keysize:
      key_index = 0

    result = (ord(character) - ord(key[key_index])) % 256
    output += chr(result)
         
    key_index += 1
         
  return output