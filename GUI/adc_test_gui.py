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

                adc_test_button = Gtk.Button.new_with_label("Run ADC Test")
                adc_test_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                adc_test_button.connect("clicked", self.call_adctest)
                vbox4.pack_start(adc_test_button, True, True, 0)

                hbox.pack_start(vbox4, True, True, 0) 

                
                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)

                self.show_all()

        def call_adctest(self, button):
                subprocess.check_output(["python", "doAdcTest_extPulser_DCscan.py"])


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

                #self.set_opacity(0)
                subw = AnotherWindow()
                
        def updateGUI():
                while Gtk.events_pending():
                        Gtk.main_iteration(False)

        def wait_5s(self, entry):
                for i in range(5):
                        print "waiting..."
                        time.sleep(5)
                        updateGUI()     
    

win = ChipTestWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
