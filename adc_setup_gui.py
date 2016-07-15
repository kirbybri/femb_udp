import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import sys
import subprocess
import importlib

class OutputWindow(Gtk.Window):

        def __init__(self, data):
                Gtk.Window.__init__(self, title="View Output")
		self.set_size_request(400,800)
                self.data = data
                self.grid = Gtk.Grid()
                self.add(self.grid)
                self.create_textview()
                #self.save_button()

                self.show_all()

        def create_textview(self):
                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)
                self.grid.attach(scrolledwindow, 0, 1, 3, 1)

                self.textview = Gtk.TextView()
                self.textbuffer = self.textview.get_buffer()
                self.textbuffer.set_text(self.data)
                scrolledwindow.add(self.textview)
                #print "Configuring board..."
                #Gtk.main_quit()



class ConfigWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="Config Window")
                self.connect("destroy", lambda x: Gtk.main_quit())
                self.show_all()

                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                config_label = Gtk.Label("Board Configuration")
                vbox.pack_start(config_label, True, True, 0)

                #board_types = Gtk.ListStore(str)
                #boards = ["35t", "acdTest"]
                #for board in boards:
                #       board_types.append([board])

                #self.config_combo = Gtk.ComboBoxText()
                #self.config_combo.set_entry_text_column(0)
                #for board in boards:
                #        self.config_combo.append_text(board)

                #vbox.pack_start(self.config_combo, False, False, 0)

                config_button = Gtk.Button.new_with_label("Board Config")
                config_button.connect("clicked", self.call_configboard)
                vbox.pack_start(config_button, True, True, 0)

                init_button = Gtk.Button.new_with_label("Init Board")
                init_button.connect("clicked", self.call_init)
                vbox.pack_start(init_button, True, True, 0)

                self.add(vbox)

        
        def call_configboard(self,button):
                #config_type = str(self.config_combo.get_active_text())
                global config_type
		config_type = "adcTest"
                mod = "femb_config_" + config_type
                #mod = "femb_config_adcTest"

                global config
                config = importlib.import_module(mod)

		Gtk.main_quit()

	def call_init(self,button):
                data = subprocess.check_output(["python", "init_femb.py", config_type])
                subw = OutputWindow(data)

                #Gtk.main_quit()
                


win = ConfigWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
