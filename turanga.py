# -*- coding: utf-8 -*-

import sys
import os
import hashlib
import getpass
from time import time
from cipher import packer
from cipher import utils

def get_key():
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

   return key

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
   print " |-- Turanga 2.1"
   print " |"
   print " |-- Simple and secure encryption tool"
   print " |"
   print " |-- @author Eduardo B R <eduardo@root404.com>"
   print " |-- @license MIT"
   print " |-- @github /0oeduardoo0/turanga"
   print ""
   print "     turanga --encode, -e <file_or_dir> <optional_output_dir>"
   print ""
   print "     turanga --decode, -d <turanga_output_folder> <optional_output_dir>"
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

      command = sys.argv[1]
      file_or_dir = sys.argv[2]

      files = []
      wbytes = 0 # written bytes
      rbytes = 0 # readed bytes
      efiles = 0 # encoded files counter

      if command == '--encode' or command == '-e':

         if not os.path.isdir(file_or_dir):
            files.append(file_or_dir)

         else:

            files.extend(utils.dir_scan(file_or_dir))

         if not os.path.exists(output_dir):
            os.makedirs(output_dir)

         key = get_key()

         print " ~ Wait please..."

         # for benchmark
         start_time = time()

         for file in files:

            source = utils.open_file(file)

            if source == False:
               continue

            efiles += 1
            result  = ''
            output  = ''

            wbytes += len(source)

            if len(file) > 30:
               print " ~ Encoding : %s..." % (file[0:30])
            else:
               print " ~ Encoding : %s..." % (file.ljust(30, '.'))

            hashed, result = packer.pack(file, source, key) # allahu akbar LoL
            rbytes += len(result)

            output_file = os.path.join(output_dir, hashed)
            utils.write_file(output_file, result)

            print " ~ Saved on : %s...%s [OK]" % (output_file[0:25], output_file[len(output_file)-5:len(output_file)])

         print ""
         print " ~ Done"
         print ""
         print " ~ Encode %s files" % (efiles)
         print " ~ Read  %0.2f KBytes" % (wbytes / 100.0)
         print " ~ Write %0.2f KBytes" % (rbytes / 100.0)

         if wbytes > 0:
            print " ~ Total bulking %0.2f%%" % (((rbytes * 100.0) / wbytes) - 100.0)

         print " ~ Elapsed time %0.2f seconds" % (time() - start_time)
         print ""
         print " ~ Output writed on %s\n" % (output_dir)


      elif command == '--decode' or command == '-d':

         if not os.path.isdir(file_or_dir):
            files.append(file_or_dir)

         else:

            files.extend(utils.dir_scan(file_or_dir))

         if not os.path.exists(output_dir):
            os.makedirs(output_dir)

         file_counter = 0

         key = get_key()

         print " ~ Wait please..."

         # for benchmark
         start_time = time()

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

            if len(file) > 30:
               print "Saved %s..." % (file[0:30]),
            else:
               print "Saved %s..." % (file.ljust(30, '.')),
         
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
         print " ~ Read  %0.2f KBytes" % (wbytes / 100.0)
         print " ~ Write %0.2f KBytes" % (rbytes / 100.0)
      
         if wbytes > 0:
            print " ~ %0.2f%% of encoded volume" % ((rbytes * 100.0) / wbytes)

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