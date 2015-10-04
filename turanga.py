# -*- coding: utf-8 -*-

import sys
import os
import hashlib
import getpass
from time import time
from cipher import packer
from cipher import utils

# for benchmark
start_time = time()

"""
      argv_error(argument)

      Function to show a message when an argument is missing

      @param string argument : Missing argument

      @return void
"""
def argv_error(argument):
   print " ~ [FAIL] Missing argument <%s>" % (argument)
   sys.exit()

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

try:

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

      print "|-- Turanga 2.0"
      print ""

      key = ""

      # to prevent an empty key
      while key == "":
         key  = getpass.getpass(" ~ Key: ")
         vkey = getpass.getpass(" ~ Confirm Key: ")

         if key != vkey:
            print "\n ~ [FAIL] Keys do not match!\n"
            key = ""

      print ""

      command = sys.argv[1]
      file_or_dir = sys.argv[2]

      files = []
      wbytes = 0 # written bytes
      rbytes = 0 # readed bytes

      if command == 'encode' or command == 'e':

         if not os.path.isdir(file_or_dir):
            files.append(file_or_dir)

         else:

            files.extend(utils.dir_scan(file_or_dir))

         if not os.path.exists(output_dir):
            os.makedirs(output_dir)

         for file in files:

            source = utils.open_file(file)

            if source == False:
               continue

            result = ''
            output = ''

            wbytes += len(source)

            print " ~ Encoding %s..." % (file[0:60])
            hashed, result = packer.pack(file, source, key) # allahu akbar LoL

            rbytes += len(result)

            utils.write_file(os.path.join(output_dir, hashed), result)

         print ""
         print " ~ Done"
         print ""
         print " ~ Encode %s files" % (len(files))
         print " ~ Read  %s KBytes" % (wbytes / 100)
         print " ~ Write %s KBytes" % (rbytes / 100)

         if wbytes > 0:
            print " ~ Total bulking %s%%" % ((rbytes * 100) / wbytes)

         print " ~ Elapsed time %0.2f seconds" % (time() - start_time)
         print ""
         print " ~ Output writed on %s\n" % (output_dir)


      elif command == 'decode' or command == 'd':

         if not os.path.isdir(file_or_dir):
            files.append(file_or_dir)

         else:

            files.extend(utils.dir_scan(file_or_dir))

         if not os.path.exists(output_dir):
            os.makedirs(output_dir)

         file_counter = 0

         for _file in files:

            source = utils.open_file(_file)

            if source == False:
               continue

            print " ~ Unpack... ",

            ok, error, file, content = packer.unpack(source, key)

            if not ok:

               if error == packer.INVALID_FILE_ERR:
                  print "[FAIL] Is not a turanga file %s..." % (_file[0:30])
                  continue

               if error == packer.INVALID_KEY_ERR:
                  print "[FAIL] Invalid key for %s..." % (_file[0:30])
                  continue

            print "[OK]  ",

            # get the original file name
            file = os.path.join(output_dir, file)

            wbytes += len(source)
            rbytes += len(content)

            output_file_dir = os.path.dirname(file)

            print "Saved %s..." % (file[0:30]),
         
            if not os.path.exists(output_file_dir):
               os.makedirs(output_file_dir)

            utils.write_file(file, content) # save file

            print " [OK]"
            file_counter += 1


         print ""
         print " ~ Done"
         print ""
         print " ~ Scanning %s files" % (len(files))
         print " ~ Decode %s files" % (file_counter)
         print " ~ Read  %s KBytes" % (wbytes / 100)
         print " ~ Write %s KBytes" % (rbytes / 100)
      
         if wbytes > 0:
            print " ~ %s%% of encoded volume" % ((rbytes * 100) / wbytes)

         if(file_counter < len(files)):
            print " ~ Some files was not decoded, maybe, a bad key was used"
            
         print " ~ Elapsed time %0.2f seconds" % (time() - start_time)
         print ""
         print " ~ Output writed on %s\n" % (output_dir)

      else:

         show_help()
except KeyboardInterrupt:
   print "\n\n|-- stoped"

print "|-- bye"