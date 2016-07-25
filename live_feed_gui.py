from datetime import datetime, date, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import sys
import importlib
import os
#import importlib
#from femb_config_35t import FEMB_CONFIG
#from setup_config import *
from setup_gui import *

config_type = os.environ["CONFIG_TYPE"]
mod = "femb_config_" + config_type
config = importlib.import_module(mod)

from femb_rootdata import FEMB_ROOTDATA
from femb_udp_cmdline import FEMB_UDP
import subprocess
import time

class DataViewWindow(Gtk.Window):

        def __init__(self, data):
                Gtk.Window.__init__(self, title="View Data Output")
		self.set_size_request(400,900)
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


class ChipTestWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="Live Feed")

                self.femb_config = config.FEMB_CONFIG()
                self.femb_rootdata = FEMB_ROOTDATA()
                self.femb_udp = FEMB_UDP()


                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                self.add(hbox)
                vbox5= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                
                plot_data_button = Gtk.Button.new_with_label("Plot Data")
                plot_data_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                plot_data_button.connect("clicked", self.call_plot_data)
                vbox5.pack_start(plot_data_button, True, True, 0)

                plot_fft_button = Gtk.Button.new_with_label("Plot FFT")
                plot_fft_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                plot_fft_button.connect("clicked", self.call_plot_fft)
                vbox5.pack_start(plot_fft_button, True, True, 0)

                run_all_chan_button = Gtk.Button.new_with_label("Test all channels")
                run_all_chan_button.connect("clicked", self.call_run_all)
                vbox5.pack_start(run_all_chan_button, True, True, 0)

		hbox.pack_start(vbox5, True, True, 0)

            	vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		asicVal_label = Gtk.Label("ASIC")
                vbox2.pack_start(asicVal_label, True, True, 0)
                self.asicVal_combo = Gtk.ComboBoxText()
                self.asicVal_combo.set_entry_text_column(0)
                #for i in range(8):
                	#self.asicVal_combo.append_text(str(i))
		self.asicVal_combo.append_text(str(0))
                vbox2.pack_start(self.asicVal_combo,False,False,0)

                channelVal_label = Gtk.Label("Channel")
                vbox2.pack_start(channelVal_label, True, True, 0)
                self.channelVal_combo = Gtk.ComboBoxText()
                self.channelVal_combo.set_entry_text_column(0)
                for i in range(16):
                        self.channelVal_combo.append_text(str(i))
                vbox2.pack_start(self.channelVal_combo,False,False,0)
	
                selectChannel_button = Gtk.Button.new_with_label("Select Channel")
                selectChannel_button.connect("clicked", self.call_selectChannel)
                vbox2.pack_start(selectChannel_button, True, True, 0)

		hbox.pack_start(vbox2, True, True, 0)
                
                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)

                self.show_all()



        def call_plot_data(self, button):
                data = subprocess.check_output(["python", "pyroot_plot.py"])
                #subw = DataViewWindow(data)

        def call_plot_fft(self, button):
                data = subprocess.check_output(["python", "plot_fft.py"])
                #subw = DataViewWindow(data)


        def call_selectChannel(self, button):
                asic = str(self.asicVal_combo.get_active_text())
                channel = str(self.channelVal_combo.get_active_text())
                #self.femb_config.selectChannel(asic, channel)
		data = subprocess.check_output(["python", "select_channel.py",config_type, asic, channel])
		subw = DataViewWindow(data)


        def call_run_all(self, button):
                asicval = str(0)
                for i in range(16):
                        chanval = str(i)
                        data = subprocess.check_output(["python", "select_channel.py",config_type, asicval, chanval])
                        subprocess.check_output(["python", "pyroot_plot.py"])
                        subw = DataViewWindow(data)


win = ChipTestWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
