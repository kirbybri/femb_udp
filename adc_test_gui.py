from datetime import datetime, date, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
#from femb_config_35t import FEMB_CONFIG
#from setup_config import *
#from setup_gui import *
from adc_setup_gui import *
from femb_rootdata import FEMB_ROOTDATA
from femb_udp_cmdline import FEMB_UDP
import subprocess
import time

class OutputWindow(Gtk.Window):

        def __init__(self, data):
                Gtk.Window.__init__(self, title="View Output")
                self.set_size_request(400,600)
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
		start = self.textbuffer.get_start_iter()
		end = self.textbuffer.get_end_iter()
		#self.textbuffer.unpdate_idletasks()
		

		#for i[0:-1] in self.data:
		#	print i

		#lines = self.textbuffer.get_line_count()
		
		#if self.data[0:18] == "This chip is good.":
		good_match = start.forward_search("This ASIC is good.",0,end)
		print good_match
		if good_match != None:
			self.textview.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0.0,1.0,0.0,1.0))

		#elif self.data[0:17] == "This chip is bad.":
		#elif text.count("This chip is bad.") == 1:
		bad_match = start.forward_search("This ASIC is bad.",0,end)
		if bad_match != None:
			self.textview.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(1.0,0.0,0.0,1.0))
                
		scrolledwindow.add(self.textview)

                #Gtk.main_quit()




class AnotherWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="Testing Window")
                self.connect("destroy", lambda x: Gtk.main_quit())
                self.set_size_request(100,100)
                self.femb_config = config.FEMB_CONFIG()
                self.femb_rootdata = FEMB_ROOTDATA()
                self.femb_udp = FEMB_UDP()

                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                self.add(hbox)
                vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		global j
		j = 0	
                for files in os.walk("slope_hists"):
			#print len(files[2])
			for x in files[2]:#range(0,len(files[2]),1)
				#print x[-9:-5]
				if str(sn1) == x[-9:-5]:
					#print "Matching"
					#print x[6:8]
					#print "..."
				#if i == x[6:7]
					for i in range(0,100,1):
						#print i
						#if "/slopes_" + str(i) + "_" + str(sn1) + ".root" == True:
						if str(i) == x[6:8]:
							if i+1 >= j:
								j = i+1
								#print j
							else:
								j=j
								#print j
							#break
						elif str(i)+"_" == x[6:8]:
							#print i
							#global j
							if i+1 >= j:
								j = i+1
								#print j
							else:
								j=j
								#print j
							#break
					
	 
		self.entry = Gtk.Entry()
		self.entry.set_text(str(j))
                self.entry.modify_base(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))
                #self.entry1.modify_fg(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))
                #self.entry1.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0,1,0,1))
                #self.entry1.modify_text(Gtk.StateType.NORMAL,Gdk.Color(0,1,0))  
                label = Gtk.Label("Run number:")
                vbox2.pack_start(label, True, True, 0)
                vbox2.pack_start(self.entry, True, True, 0)



		dotest_button = Gtk.Button.new_with_label("Do ADC Test")
                dotest_button.connect("clicked", self.call_dotest)
                vbox2.pack_start(dotest_button, True, True, 0)

       		analysis_button = Gtk.Button.new_with_label("Do Slope Analysis")
                analysis_button.connect("clicked", self.call_analysis)
                vbox2.pack_start(analysis_button, True, True, 0)


                #button = Gtk.CheckButton("Plot Waveform")
                #button.connect("toggled", self.call_plot, "Plot Waveform")
                #vbox2.pack_start(button, True, True, 2)

                #button = Gtk.CheckButton("Plot FFT")
                #button.connect("toggled", self.call_plot)
                #vbox2.pack_start(button, True, True, 2)

                hbox.pack_start(vbox2, True, True, 0)
                
                scrolledwindow = Gtk.ScrolledWindow()
                scrolledwindow.set_hexpand(True)
                scrolledwindow.set_vexpand(True)

                self.show_all()

        #def call_plot(self, button, name):
	#	if button.get_active():
	#		state = "on"
	#		if name == "Plot Waveform":
	#			data = subprocess.check_output(["python", "pyroot_plot.py"])

                #data = subprocess.check_output(["python", "pyroot_plot.py"])

                #subw = DataViewWindow(data)

        #def call_plot_fft(self, button):
        #        data = subprocess.check_output(["python", "plot_fft.py"])
        #        subw = DataViewWindow(data)

	def call_dotest(self, button):
		#data = subprocess.check_call(['python','doAdcTest_extPulser_DCscan.py'])
		#data = subprocess.check_output(["python","slope_hist.py",str(1.5)])
		data1 = subprocess.check_call(['python','pyroot_all.py', str(sn1), str(j)])
		#if data1 == 0:
		#	sys.exit()
		data = subprocess.check_output(["python", "adcTest_plots.py", str(j),str(sn1)])
		#print sn1
		#data = "Hello world. \nThis is a good chip."
		subw = OutputWindow(str(data))

	def call_analysis(self, button):
                data = subprocess.check_call(['python', 'analysis_hist.py', str(sn1), str(j)])
                


class ChipTestWindow(Gtk.Window):

        def __init__(self):
                Gtk.Window.__init__(self, title="ADC Test Log")
                
                
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
                global sn1
		sn1 = self.entry1.get_text()
                self.tester_name = self.entry5.get_text()
                self.date = self.entry6.get_text()
                self.time = self.entry7.get_text()
                
                sn1_s = 'Serial Number: ' + sn1 + '\n'
                tester_name_s = 'Tester Name: ' + self.tester_name + '\n'
                datetime = self.date + ' ' + self.time + '\n'
                f = open('test_information', 'a')
                f.write(sn1_s)
                f.write(tester_name_s)
                f.write(datetime)
                f.close()

                #data1 = subprocess.check_output(["python", "doAdcTest_extPulser_DCscan.py"])
                #data2 = subprocess.check_output(["python", "pyroot_plot.py"])

                #subw = OutputWindow(data1)  
                #subw = DataViewWindow(data2)
		subw = AnotherWindow()
                    
    

win = ChipTestWindow()
#win.update_idletasks()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

