from datetime import datetime, date, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from femb_config_35t import FEMB_CONFIG
from femb_rootdata import FEMB_ROOTDATA
from femb_udp_cmdline import FEMB_UDP
import subprocess
import time

##### Here is a new window that pops up so that you can view the data as it is processed. There is a save button that will save the data to a text file

class DataViewWindow(Gtk.Window):

        def __init__(self, data):
                Gtk.Window.__init__(self, title="View Data Output")
                self.data = data
                self.grid = Gtk.Grid()
                self.add(self.grid)
                self.create_textview()
                self.save_button()
                
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


        def save_button(self):
                save = Gtk.Button.new_with_label("Save Data")
                save.connect("clicked", self.save_data)
                self.grid.attach(save, 0, 2, 1, 1)

        def save_data(self, button):
                
                input_data = self.data + '\n'
                f = open('Saved_Data','a') 
                
                f.write(input_data)
                f.write('\n')                

                f.close()

##### This opnes a new window once you hit start test. This will get rid of the inital window that takes the tester and chip information. Here you can start running test that you would like on the chips.

class AnotherWindow(Gtk.Window):
        def __init__(self):
                Gtk.Window.__init__(self, title="Testing Window")
                self.connect("destroy", lambda x: Gtk.main_quit())

                self.femb_config = FEMB_CONFIG()
                self.femb_rootdata = FEMB_ROOTDATA()
                self.femb_udp = FEMB_UDP()


                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                self.add(hbox)
                vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                
                gainVal_label = Gtk.Label("Gain")
                vbox2.pack_start(gainVal_label, True, True, 0)
                self.gainVal_combo = Gtk.ComboBoxText()
                self.gainVal_combo.set_entry_text_column(0)
                for i in range(4):
                        self.gainVal_combo.append_text(str(i))
                vbox2.pack_start(self.gainVal_combo,False,False,0)

                shapeVal_label = Gtk.Label("Shape")
                vbox2.pack_start(shapeVal_label, True, True, 0)
                self.shapeVal_combo = Gtk.ComboBoxText()
                self.shapeVal_combo.set_entry_text_column(0)
                for i in range(4):
                        self.shapeVal_combo.append_text(str(i))
                vbox2.pack_start(self.shapeVal_combo,False,False,0)

                baseVal_label = Gtk.Label("Base")
                vbox2.pack_start(baseVal_label, True, True, 0)
                self.baseVal_combo = Gtk.ComboBoxText()
                self.baseVal_combo.set_entry_text_column(0)
                self.baseVal_combo.append_text('0')
                self.baseVal_combo.append_text('1')
                vbox2.pack_start(self.baseVal_combo,False,False,0)


                asicVal_label = Gtk.Label("ASIC")
                vbox2.pack_start(asicVal_label, True, True, 0)
                self.asicVal_combo = Gtk.ComboBoxText()
                self.asicVal_combo.set_entry_text_column(0)
                for i in range(8):
                        self.asicVal_combo.append_text(str(i))
                vbox2.pack_start(self.asicVal_combo,False,False,0)

                channelVal_label = Gtk.Label("Channel")
                vbox2.pack_start(channelVal_label, True, True, 0)
                self.channelVal_combo = Gtk.ComboBoxText()
                self.channelVal_combo.set_entry_text_column(0)
                for i in range(16):
                        self.channelVal_combo.append_text(str(i))
                vbox2.pack_start(self.channelVal_combo,False,False,0)

                register_label = Gtk.Label("Register (0 - 666)")
                vbox2.pack_start(register_label, True, True, 0)
                self.register_entry = Gtk.Entry()
                vbox2.pack_start(self.register_entry, True, True, 0)

                self.entry5 = Gtk.Entry()
                data_label = Gtk.Label("Data Value")
                vbox2.pack_start(data_label, True, True, 0)
                vbox2.pack_start(self.entry5, True, True, 0)


                hbox.pack_start(vbox2, True, True, 0)
                vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                
                resetBoard_button = Gtk.Button.new_with_label("Reset Board")
                resetBoard_button.connect("clicked", self.call_resetBoard)
                vbox3.pack_start(resetBoard_button, True, True, 0)

                initBoard_button = Gtk.Button.new_with_label("Init Board")
                initBoard_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                initBoard_button.connect("clicked", self.call_initBoard)
                vbox3.pack_start(initBoard_button, True, True, 0)

                selectChannel_button = Gtk.Button.new_with_label("Select Channel")
                selectChannel_button.connect("clicked", self.call_selectChannel)
                vbox3.pack_start(selectChannel_button, True, True, 0)


                configFeAsic_button = Gtk.Button.new_with_label("Config Front End Asic")
                configFeAsic_button.connect("clicked", self.call_configFeAsic)
                vbox3.pack_start(configFeAsic_button, True, True, 0)

                syncADC_button = Gtk.Button.new_with_label("Sync ADC")
                syncADC_button.connect("clicked", self.call_syncADC)
                vbox3.pack_start(syncADC_button, True, True, 0)

                testUnsync_button = Gtk.Button.new_with_label("Test Unsync")
                testUnsync_button.connect("clicked", self.call_testUnsync)
                vbox3.pack_start(testUnsync_button, True, True, 0)

                fixUnsync_button = Gtk.Button.new_with_label("Fix Unsync")
                fixUnsync_button.connect("clicked", self.call_fixUnsync)
                vbox3.pack_start(fixUnsync_button, True, True, 0)
                hbox.pack_start(vbox3, True, True, 0) 


                vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                


                record_channel_button = Gtk.Button.new_with_label("Record Channel Data")
                record_channel_button.connect("clicked", self.call_channel_record)
                vbox4.pack_start(record_channel_button, True, True, 0)
             
                record_run_button = Gtk.Button.new_with_label("Record Data Run")
                record_run_button.connect("clicked", self.call_channel_record)
                vbox4.pack_start(record_run_button, True, True, 0)

                record_binary_button = Gtk.Button.new_with_label("Record Binary Data")
                record_binary_button.connect("clicked", self.call_binary_record)
                vbox4.pack_start(record_binary_button, True, True, 0)

                validation_data_button = Gtk.Button.new_with_label("Take Validation Data Set")
                validation_data_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                validation_data_button.connect("clicked", self.call_validation_data)
                vbox4.pack_start(validation_data_button, True, True, 0)

                hbox.pack_start(vbox4, True, True, 0) 


                vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                
                
                get_data_button = Gtk.Button.new_with_label("Get Data")
                get_data_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                get_data_button.connect("clicked", self.call_get_data)
                vbox5.pack_start(get_data_button, True, True, 0)


                measureNoise_button = Gtk.Button.new_with_label("Measure Noise")
                measureNoise_button.connect("clicked", self.call_measureNoise)
                vbox5.pack_start(measureNoise_button, True, True, 0)

                plot_data_button = Gtk.Button.new_with_label("Plot Data")
                plot_data_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                plot_data_button.connect("clicked", self.call_plot_data)
                vbox5.pack_start(plot_data_button, True, True, 0)

                #plot_fft_button = Gtk.Button.new_with_label("Plot FFT")
                #plot_fft_button.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                #plot_fft_button.connect("clicked", self.call_plot_fft)
                #vbox5.pack_start(plot_fft_button, True, True, 0)

                read_reg_button = Gtk.Button.new_with_label("Read Register")
                read_reg_button.connect("clicked", self.call_read_reg)
                vbox5.pack_start(read_reg_button, True, True, 0)

                write_reg_button = Gtk.Button.new_with_label("Write Register")
                write_reg_button.connect("clicked", self.call_write_reg)
                vbox5.pack_start(write_reg_button, True, True, 0)

                hbox.pack_start(vbox5, True, True, 0)
                
                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)

                self.show_all()



        def call_resetBoard(self, button):
                self.femb_config.resetBoard()

        def call_initBoard(self, button):
                self.femb_config.initBoard()

        def call_selectChannel(self, button):
                asic = int(self.asicVal_combo.get_active_text())
                channel = int(self.channelVal_combo.get_active_text())
                self.femb_config.selectChannel(asic, channel)

        def call_configFeAsic(self, button):
                gain = int(self.gainVal_combo.get_active_text())
                shape = int(self.shapeVal_combo.get_active_text())
                base = int(self.baseVal_combo.get_active_text())
                self.femb_config.configFeAsic(gain, shape, base)

        def call_syncADC(self, button):
                self.femb_config.syncADC()

        def call_testUnsync(self, button):
                asic = int(self.asicVal_combo.get_active_text())
                self.femb_config.testUnsync(asic)

        def call_fixUnsync(self, button):
                asic = int(self.asicVal_combo.get_active_text())
                self.femb_config.fixUnsync(asic)      

        def call_channel_record(self, button):
                asic = int(self.asicVal_combo.get_active_text())
                channel = int(self.channelVal_combo.get_active_text())
                ch = asic*16 + channel
                self.femb_rootdata.record_channel_data(ch)

        def call_run_record(self, button):
                self.femb_rootdata.record_data_run()

        def call_binary_record(self, button):
                self.femb_udp.record_binary_data(10)

        def call_validation_data(self, button):
                subprocess.check_output(["python", "take_validation_data_set.py"])

        def call_get_data(self, button):
                data = subprocess.check_output(["python", "get_data.py"])
                subw = DataViewWindow(data)

        def call_measureNoise(self, button):
                data = subprocess.check_output(["python", "measureNoise.py"])
                subw = DataViewWindow(data)

        def call_plot_data(self, button):
                data = subprocess.check_output(["python", "plot_data_fast.py"])
                subw = DataViewWindow(data)

        #def call_plot_fft(self, button):
        #        data = subprocess.check_output(["python", "plot_fft_fast.py"])
        #        subw = DataViewWindow(data)

        def call_read_reg(self, button):
                data = subprocess.check_output(["python", "read_reg.py"])
                subw = DataViewWindow(data)

        def call_write_reg(self, button):
                data = subprocess.check_output(["python", "write_reg.py"])
                subw = DataViewWindow(data)

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
                self.entry2.connect("activate", self.wait_5s)
                #while True:                        
                #        time.sleep(30)
                inputfile = open('Saved_Data', "r")
                lines = 0
                #line = inputfile.readlines()
                for line in inputfile:
                        lines += 1
                        line = line.strip('\n')
                
                last_line = line
                print last_line
                #print "Hi"
                if last_line == "Hello World":
                        print "yes"
                        self.entry2.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0.0,1.0,0.0,1.0))
                elif last_line != "Hello World":
                        self.entry2.override_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(1.0,0.0,0.0,1.0))

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
