# -*- coding: utf-8 -*-

import sys
import os

try:   
   from gi.repository import Gtk

except:
   print "Error: python-gtk library not found"

class TurangaGtk:

   def __init__(self):
      
      glade_file = os.path.join(os.path.dirname(__file__), 'glade', 'turanga-gtk.glade')

      #Set the Glade file
      self.builder = Gtk.Builder()
      self.builder.add_from_file(glade_file)

      events = {
           "on_quit": Gtk.main_quit
         , "on_open_file": self.open_file
         , "on_encode": self.encode
      }

      self.builder.connect_signals(events)
      self.main_window = self.builder.get_object("main_window")
      self.main_window.show_all()

      self.txt_output = self.builder.get_object("txt_output").get_buffer()
      self.output_counter = 0

      self.source = ""
      self.output_dir = ""

   def main(self):
      Gtk.main()

   def output(self, text):
      start_iter = self.txt_output.get_start_iter()
      end_iter = self.txt_output.get_end_iter()
      last = self.txt_output.get_text(start_iter, end_iter, True)
      text = str(self.output_counter) + ": " + text + "\n" + last
      self.txt_output.set_text(text)
      self.output_counter += 1

   def open_file(self, widget, icon_pos, u_data):

      if icon_pos.value_name == "GTK_ENTRY_ICON_PRIMARY":
         action = Gtk.FileChooserAction.SELECT_FOLDER
      else:
         action = Gtk.FileChooserAction.OPEN

      dialog = Gtk.FileChooserDialog(
         "Please choose a file or dir",
            widget.get_toplevel(),
            action,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK
            )
      )

      response = dialog.run()

      if response == Gtk.ResponseType.OK:
         _file = dialog.get_filename()
         dialog.destroy()
            
         text_box = self.builder.get_object("txt_file_or_dir")
         text_box.set_text(_file)
         self.source = _file

         _output = os.path.join(os.path.dirname(_file), "turanga_output")
         text_box_2 = self.builder.get_object("txt_output_dir")
         text_box_2.set_text(_output)
         self.output_dir = _output

      else:
         dialog.destroy()

   def get_pass(self):

      entry = self.builder.get_object("txt_password")
      text  = entry.get_text()

      if text == "":

         self.output("You need write a password")
         return False

      return text

   def encode(self, widget):

      passw = self.get_pass()

      if not passw:
         return

      if self.source == "":
         self.output("No file or dir to encode")
         return

      if self.output_dir == "":
         self.output("No output dir")
         return

if __name__ == "__main__":

   app = TurangaGtk()
   app.main()