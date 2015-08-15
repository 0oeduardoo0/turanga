# -*- coding: utf-8 -*-

import sys
import os
import hashlib
from time import time
from cipher import algorithm

start_time = time()

def open_file_error(file):
   print "Can not open %s" % (file)

def argv_error(argument):
   print "Missing argument <%s>" % (argument)
   sys.exit()

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

def open_file(file):
   try:
      file_obj = open(file)
      result = file_obj.read()
      file_obj.close()
      return result
   except:
      open_file_error(file)
      return False

def write_file(file, content):
   output_file = open(file, 'w')
      
   output_file.truncate()
   output_file.write(content)
   output_file.close()

def show_help():
   print ""
   print " |-- Turanga 2.0"
   print " |"
   print " |-- Simple and secure encryption tool"
   print " |"
   print " |-- @author Eduardo B R <eduardo@root404.com>"
   print " |-- @license MIT"
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
      argv_error("file_or_dir")

   try:
      sys.argv[3]
   except:
      argv_error("key")

   try:
      output_dir = sys.argv[4]
   except:
      output_dir = 'turanga_output'

   command = sys.argv[1]
   file_or_dir = sys.argv[2]
   key = sys.argv[3]

   metadata = '=\n' + algorithm.encode('_TURANGA_VERIFY_KEY_', key) + '\n\n'
   files = []
   _bytes = 0
   rbytes = 0

   if command == 'encode':

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

         file_hash = hashlib.sha224(file).hexdigest()
         result = ''
         output = ''

         _bytes += len(source)

         print "Encoding %s..." % (file)
         result = algorithm.encode(source, key)

         rbytes += len(result)

         write_file(os.path.join(output_dir, file_hash), result)

         metadata += '=\n' + file_hash + '\n' + algorithm.encode(file, key) + '\n\n'

      metadata_file = open(os.path.join(output_dir, 'data_information'), 'w')
   
      metadata_file.truncate()
      metadata_file.write(metadata.strip())
      metadata_file.close()

      print ""
      print "Done"
      print ""
      print "Encode %s files" % (len(files))
      print "Read  %s KBytes" % (_bytes / 100)
      print "Write %s KBytes" % (rbytes / 100)
      print "Total bulking %s%%" % ((rbytes * 100) / _bytes)
      print "Elapsed time %0.2f seconds" % (time() - start_time)
      print ""
      print "Output writed on %s" % (output_dir)


   elif command == 'decode':

      if not os.path.isdir(file_or_dir):
         print "Error! I need a turanga output directory..."
         sys.exit()

      else:

         metadata_file = os.path.join(file_or_dir, 'data_information')

         if not os.path.exists(output_dir):
            os.makedirs(output_dir)

         if not os.path.isfile(metadata_file):
            print "Missing data_information file";
            sys.exit()

         metadata_file = open(metadata_file)
         metadata = metadata_file.read()
         metadata_file.close()

         metadata = metadata.split('=');
         key_signature = metadata[1].strip();

         #print metadata
         #sys.exit()

         print "Verifing key signature\n\n%s\n" % (key_signature)
         
         try:
            verify_key = algorithm.decode(key_signature, key)
         except:
            verify_key = False

         if not verify_key == '_TURANGA_VERIFY_KEY_':
            print "Invalid key"
            sys.exit()

         for file in metadata[2:]:
            file_data = file.strip().split('\n')
            file_origin = os.path.join(file_or_dir, file_data[0])
            file_output = os.path.join(output_dir, algorithm.decode(file_data[1], key))

            source = open_file(file_origin)

            if source == False:
               continue

            _bytes += len(source)

            print "Decoding %s..." % (file_output)
            result = algorithm.decode(source, key)

            rbytes += len(result)

            output_file_dir = os.path.dirname(file_output)
            if not os.path.exists(output_file_dir):
               os.makedirs(output_file_dir)

            write_file(file_output, result)

         print ""
         print "Done"
         print ""
         print "Decode %s files" % (len(metadata) - 2)
         print "Read  %s KBytes" % (_bytes / 100)
         print "Write %s KBytes" % (rbytes / 100)
         print "%s%% of encoded volume" % ((rbytes * 100) / _bytes)
         print "Elapsed time %0.2f seconds" % (time() - start_time)
         print ""
         print "Output writed on %s" % (output_dir)

   else:
      show_help()