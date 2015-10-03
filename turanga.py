# -*- coding: utf-8 -*-

import sys
import os
import hashlib
import getpass
from time import time
from cipher import algorithm

# for benchmark
start_time = time()

"""
      open_file_error(file)

      Function to show an error when a file was not be read

      @param string file : name or path to the file

      @return void
"""
def open_file_error(file):
   print "Can not open %s" % (file)

"""
      argv_error(argument)

      Function to show a message when an argument is missing

      @param string argument : Missing argument

      @return void
"""
def argv_error(argument):
   print "Missing argument <%s>" % (argument)
   sys.exit()

"""
   
      dir_scan(_dir)

      Function to scan (recursively) some path

      @param string _dir : Absolute or relative path to directory

      @return Array
"""
def dir_scan(_dir):
   files = []

   print "Scanning %s..." % (_dir)

   for root, subdirs, filenames in os.walk(_dir):
      for subdir in subdirs:
         files.extend(dir_scan(os.path.join(_dir, subdir)))

      for filename in filenames:
         filename = os.path.join(_dir, filename)
         if os.path.isfile(filename):
            files.append(filename)

   return files

"""
      open_file(file)

      Function to try to read the bytes of a file, return false
      and sends a message if something go wrong

      @param string file : absolute or relative path to the file

      @return mixed
"""
def open_file(file):
   try:
      file_obj = open(file)
      result = file_obj.read()
      file_obj.close()
      return result
   except:
      open_file_error(file)
      return False

"""
      write_file(file, content)

      Function to overwrite some file with some content

      @param string file : path to file to overwrite (or create)
      @param string content : content to write
"""
def write_file(file, content):
   output_file = open(file, 'w')
      
   output_file.truncate()
   output_file.write(content)
   output_file.close()

"""
      show_help()

      Function to print the help menu

      @return void
"""
def show_help():
   print ""
   print " |-- Turanga 2.0"
   print " |"
   print " |-- Simple and secure encryption tool"
   print " |"
   print " |-- @author Eduardo B R <eduardo@root404.com>"
   print " |-- @license MIT"
   print " |-- @github /0oeduardoo0/turanga"
   print ""
   print "     turanga encode, e <file_or_dir> <optional_output_dir>"
   print ""
   print "     turanga decode, d <turanga_output_folder> <optional_output_dir>"
   print ""
   sys.exit()

if __name__ == "__main__":

   try:
      sys.argv[1]
   except:
      show_help()

   try:
      sys.argv[2]
   except:
      argv_error("file_or_dir") # i need the fucking file or dir to encode/decode xD

   try:
      output_dir = sys.argv[3]
   except:
      output_dir = 'turanga_output'

   key = ""

   # to prevent an empty key
   while key == "":
      key  = getpass.getpass("Encryption Key: ")
      vkey = getpass.getpass("Confirm Key: ")

      if key != vkey:
         print "Keys do not match!"
         key = ""

   command = sys.argv[1]
   file_or_dir = sys.argv[2]

   files = []
   wbytes = 0 # written bytes
   rbytes = 0 # readed bytes

   if command == 'encode' or command == 'e':

      if not os.path.isdir(file_or_dir):
         files.append(file_or_dir)

      else:

         files.extend(dir_scan(file_or_dir))

      if not os.path.exists(output_dir):
         os.makedirs(output_dir)

      for file in files:

         source = open_file(file)

         if source == False:
            continue

         # to get an output name file
         file_hash = hashlib.md5(file).hexdigest()

         # These 3 bytes indicates that this file is Turanga's encryption
         metadata  = 'trg.'
         # Encode a known piece of data to the decoder be able to verify the key
         metadata += algorithm.encode('_ALL_OK_', key) + '.'
         # encode the original file name
         metadata += algorithm.encode(file, key) + '.'

         result = ''
         output = ''

         wbytes += len(source)

         print "Encoding %s..." % (file[0:60])
         result = algorithm.encode(source, key) # allahu akbar LoL

         rbytes += len(result)

         write_file(os.path.join(output_dir, file_hash), metadata + result)

      print ""
      print "Done"
      print ""
      print "Encode %s files" % (len(files))
      print "Read  %s KBytes" % (wbytes / 100)
      print "Write %s KBytes" % (rbytes / 100)

      if wbytes > 0:
         print "Total bulking %s%%" % ((rbytes * 100) / wbytes)

      print "Elapsed time %0.2f seconds" % (time() - start_time)
      print ""
      print "Output writed on %s" % (output_dir)


   elif command == 'decode' or command == 'd':

      if not os.path.isdir(file_or_dir):
         files.append(file_or_dir)

      else:

         files.extend(dir_scan(file_or_dir))

      if not os.path.exists(output_dir):
         os.makedirs(output_dir)

      file_counter = 0

      for file in files:

         source = open_file(file)

         if source == False:
            continue

         # checking the first 3 bytes to know the type of file, 
         # to know if it is a Turanga's encryption
         if not source[0:3] == 'trg':
            print "Error! %s is not a turanga encryption" % (file)
            continue

         trg, verify_key, file_name, content = source.split('.')

         print "Verifing key... ",

         try:
            verify_key = algorithm.decode(verify_key, key)
         except:
            print "[FAIL] Invalid key for a file... skiping"
            continue

         # check These verification key
         if not verify_key == "_ALL_OK_":
            print "[FAIL] Invalid key for a file... skiping"
            continue
         else:
            print "[OK]  ",

         # get the original file name
         file_name = os.path.join(output_dir, algorithm.decode(file_name, key))

         wbytes += len(source)

         print "Decoding %s..." % (file_name[0:30]),
         result = algorithm.decode(content, key) # get the file content
         print " [OK]"

         rbytes += len(result)

         output_file_dir = os.path.dirname(file_name)
         
         if not os.path.exists(output_file_dir):
            os.makedirs(output_file_dir)

         write_file(file_name, result) # save file
         file_counter += 1


      print ""
      print "Done"
      print ""
      print "Scanning %s files" % (len(files))
      print "Decode %s files" % (file_counter)
      print "Read  %s KBytes" % (wbytes / 100)
      print "Write %s KBytes" % (rbytes / 100)
      
      if wbytes > 0:
         print "%s%% of encoded volume" % ((rbytes * 100) / wbytes)

      if(file_counter < len(files)):
         print "Some files was not decoded, maybe, a bad key was used"
            
      print "Elapsed time %0.2f seconds" % (time() - start_time)
      print ""
      print "Output writed on %s" % (output_dir)

   else:

      show_help()