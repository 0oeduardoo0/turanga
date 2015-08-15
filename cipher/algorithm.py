# -*- coding: utf-8 -*-

def encode(text, key):
   
  keysize = len(key)
  key_index = 0 
  output = ''

  for character in text:
    if key_index >= keysize:
      key_index = 0
         
    result = ord(character) + ord(key[key_index])
         
    output += ' ' + str(result)
         
    key_index += 1

  return output.strip()
      
def decode(text, key):
  
  keysize = len(key)
  key_index = 0
  output = ''

  for character in text.split(' '):
    if key_index >= keysize:
      key_index = 0

    result = int(character) - ord(key[key_index])
            
    output += chr(result)
         
    key_index += 1
         
  return output.strip()