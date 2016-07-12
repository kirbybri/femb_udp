from datetime import datetime, date, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
#from femb_config_35t import FEMB_CONFIG
#from setup_config import *
#from setup_gui import *
from adc_setup_gui import config
from femb_rootdata import FEMB_ROOTDATA
from femb_udp_cmdline import FEMB_UDP
import subprocess
import time

class OutputWindow(Gtk.Window):

        def __init__(self, data1):
                Gtk.Window.__init__(self, title="View Output")
                self.data1 = data1
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
                self.textbuffer.set_text(self.data1)
                scrolledwindow.add(self.textview)
                Gtk.main_quit()
"""
class PlottingWindow(Gtk.Window):

        def __init__(self, data2):
                Gtk.Window.__init__(self, title="View Output")
                self.data2 = data2
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
                self.textbuffer.set_text(self.data2)
                scrolledwindow.add(self.textview)
                Gtk.main_quit()
"""

class ChipTestWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="ACD Test Log")
                
                
                vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                self.add(vbox1)

                self.entry1 = Gtk.Entry()
                self.entry1.modify_base(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))
                #self.entry1.modify_fg(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))
                #self.entry1.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0,1,0,1))
                #self.entry1.modify_text(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))  
                label1 = Gtk.Label("Enter serial number from chip:")
                vbox1.pack_start(label1, True, True, 0)
                vbox1.pack_start(self.entry1, True, True, 0)

                
                self.entry5 = Gtk.Entry()
                label5 = Gtk.Label("Enter your first and last name here:")
                vbox1.pack_start(label5, True, True, 0)
                vbox1.pack_start(self.entry5, True, True, 0)
                
                date_label = Gtk.Label("Date")
                vbox1.pack_start(date_label, True, True, 0)
                self.entry6 = Gtk.Entry()
                today_date = date.today()
                today = today_date.strftime('%m/%d/%Y')
                #print (today)
                self.entry6.set_text(today)
                vbox1.pack_start(self.entry6, True, True, 0)
                
                time_label = Gtk.Label("Time")
                vbox1.pack_start(time_label, True, True, 0)
                self.entry7 = Gtk.Entry()
                current_time = datetime.today()
                t = current_time.strftime('%H:%M:%S %Z')
                self.entry7.set_text(t)
                vbox1.pack_start(self.entry7, True, True, 0)
                
                button = Gtk.Button.new_with_label("Start Test")
                button.connect("clicked", self.on_click_me_clicked)
                vbox1.pack_start(button, True, True, 0)

                
             
        def on_click_me_clicked(self, button):
                self.sn1 = self.entry1.get_text()
                self.tester_name = self.entry5.get_text()
                self.date = self.entry6.get_text()
                self.time = self.entry7.get_text()
                
                sn1_s = 'Serial Number: ' + self.sn1 + '\n'
                tester_name_s = 'Tester Name: ' + self.tester_name + '\n'
                datetime = self.date + ' ' + self.time + '\n'
                f = open('test_information', 'a')
                f.write(sn1_s)
                f.write(tester_name_s)
                f.write(datetime)
                f.close()

                #data1 = subprocess.check_output(["python", "doAdcTest_extPulser_DCscan.py"])
                data2 = subprocess.check_output(["python", "pyroot_plot.py"])

                #subw = OutputWindow(data1)  
                subw = DataViewWindow(data2)
                    
    

win = ChipTestWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
