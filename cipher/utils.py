# -*- coding: utf-8 -*-

import os

"""
   
      dir_scan(_dir)

      Function to scan (recursively) some path

      @param string _dir : Absolute or relative path to directory

      @return Array
"""
def dir_scan(_dir):
   files = []

   print " ~ Scanning %s..." % (_dir)

   for root, subdirs, filenames in os.walk(_dir):
      for subdir in subdirs:
         files.extend(dir_scan(os.path.join(_dir, subdir)))

      for filename in filenames:
         filename = os.path.join(_dir, filename)
         if os.path.isfile(filename):
            files.append(filename)

   return files


"""
      utils.open_file_error(file)

      Function to show an error when a file was not be read

      @param string file : name or path to the file

      @return void
"""
def open_file_error(file):
   print " ~ Can not open %s" % (file)


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