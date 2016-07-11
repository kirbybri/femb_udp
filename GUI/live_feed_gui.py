from datetime import datetime, date, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
#from femb_config_35t import FEMB_CONFIG
#from setup_config import *
from setup_gui import *
from femb_rootdata import FEMB_ROOTDATA
from femb_udp_cmdline import FEMB_UDP
import subprocess
import time

class ChipTestWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="Front End Chip Test Log")

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

                hbox.pack_start(vbox5, True, True, 0)
                
                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)

                self.show_all()



        def call_plot_data(self, button):
                data = subprocess.check_output(["python", "pyroot_plot.py"])
                subw = DataViewWindow(data)

        def call_plot_fft(self, button):
                data = subprocess.check_output(["python", "plot_fft.py"])
                subw = DataViewWindow(data)


win = ChipTestWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
