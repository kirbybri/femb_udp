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


class AnotherWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="Testing Window")
                self.connect("destroy", lambda x: Gtk.main_quit())

                self.femb_config = config.FEMB_CONFIG()
                self.femb_rootdata = FEMB_ROOTDATA()
                self.femb_udp = FEMB_UDP()


                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                self.add(hbox)
                vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                
############# change take validation data to ----- asic test scipt #############

                plot_data_button = Gtk.Button.new_with_label("PlotData")
                plot_data_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                plot_data_button.connect("clicked", self.call_plot_data)
                vbox4.pack_start(plot_data_button, True, True, 0)

                hbox.pack_start(vbox4, True, True, 0) 

                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)

                self.show_all()



        def call_validation_data(self, button):
                subprocess.check_output(["python", "pyroot_plot.py"])


class ChipTestWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="Front End Chip Test Log")
                
                
                vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                self.add(vbox1)

                self.entry1 = Gtk.Entry()
                self.entry1.modify_base(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))
                #self.entry1.modify_fg(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))
                #self.entry1.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0,1,0,1))
                #self.entry1.modify_text(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))  
                label1 = Gtk.Label("Enter serial number from chip 1:")
                vbox1.pack_start(label1, True, True, 0)
                vbox1.pack_start(self.entry1, True, True, 0)

                
                self.entry2 = Gtk.Entry()
                self.entry2.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0.0,0.0,1.0,1.0))
                #self.entry2.connect("activate", self.wait_5s)
                #while True:                        
                #        time.sleep(30)
                #inputfile = open('Saved_Data', "r")
                #lines = 0
                #line = inputfile.readlines()
                #for line in inputfile:
                #        lines += 1
                #        line = line.strip('\n')
                
                #last_line = line
                #print last_line
                #print "Hi"
                #if last_line == "Hello World":
                #        print "yes"
                #        self.entry2.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0.0,1.0,0.0,1.0))
                #elif last_line != "Hello World":
                #        self.entry2.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(1.0,0.0,0.0,1.0))

                label2 = Gtk.Label("Enter serial number from chip 2:")
                vbox1.pack_start(label2, True, True, 0)
                vbox1.pack_start(self.entry2, True, True, 0)
                
                self.entry3 = Gtk.Entry()
                #self.entry3.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(1.0,0.0,0.0,1.0)) 
                label3 = Gtk.Label("Enter serial number from chip 3:")
                vbox1.pack_start(label3, True, True, 0)
                vbox1.pack_start(self.entry3, True, True, 0)
                
                self.entry4 = Gtk.Entry()
                #self.entry4.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0.0,0.0,1.0,1.0)) 
                label4 = Gtk.Label("Enter serial number from chip 4:")
                vbox1.pack_start(label4, True, True, 0)
                vbox1.pack_start(self.entry4, True, True, 0)
                
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
                self.sn2 = self.entry2.get_text()
                self.sn3 = self.entry3.get_text()
                self.sn4 = self.entry4.get_text()
                self.tester_name = self.entry5.get_text()
                self.date = self.entry6.get_text()
                self.time = self.entry7.get_text()
                
                sn1_s = 'First Serial Number: ' + self.sn1 + '\n'
                sn2_s = 'Second Serial Number: ' + self.sn2 + '\n'
                sn3_s = 'Third Serial Number: ' + self.sn3 + '\n'
                sn4_s = 'Fourth Serial Number: ' + self.sn4 + '\n'
                tester_name_s = 'Tester Name: ' + self.tester_name + '\n'
                datetime = self.date + ' ' + self.time + '\n'
                f = open('test_information', 'a')
                f.write(sn1_s)
                f.write(sn2_s)
                f.write(sn3_s)
                f.write(sn4_s)
                f.write(tester_name_s)
                f.write(datetime)
                f.close()

                #self.set_opacity(0)
                subw = AnotherWindow()
 
    

win = ChipTestWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
