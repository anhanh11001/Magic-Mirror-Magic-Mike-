#!/usr/bin/env python3

import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import datetime
from Traffic_API import Trafficcheck
import pygame

class MagicWin(object):
    def __init__(self, application, ledstrip, gui_file="gui/gui.glade"):
        self.application = application
        self.gui_file = gui_file
        self.screen = Gdk.Screen.get_default()
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path('gui/css/main.css')
        Gtk.StyleContext.add_provider_for_screen(
            self.screen,
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.ledstrip = ledstrip

        try:
            self.GtkBuilder = Gtk.Builder.new_from_file(gui_file)
            self.GtkBuilder.connect_signals(self)
        except GObject.GError:
            print("Error reading {} file".format(gui_file))
            raise

        pygame.init()

        self.MainWindow = self.GtkBuilder.get_object("window1")
        self.MainWindow.set_application(self.application)

        self.stack = self.GtkBuilder.get_object("stack")

        self.MainWindow.show()

    def keyboard_event(self, window, key):
        code = key.get_keycode().keycode
        cur_screen = self.stack.get_visible_child_name()
        if code == 36: # Enter
            self.stack.set_visible_child_name("lock-screen")
        if self.is_arrow_key(code):    
            if cur_screen == "lock-screen":
                pygame.mixer.music.load('piano2.wav')
                pygame.mixer.music.play(0)
            if code == 114 or code == 39: # Right
                self.stack.set_visible_child_name("agenda")
                self.ledstrip.right(0.001)
            if code == 113 or code == 37:
                print("left")
                self.stack.set_visible_child_name("news")
                self.ledstrip.left(0.001)
            if code == 116 or code == 40:
                print("down")
                self.stack.set_visible_child_name("traffic")
            if code == 111 or code == 38: # Up
                if cur_screen == "home":
                    self.stack.set_visible_child_name("mirror-screen")
                else:
                    self.stack.set_visible_child_name("home")

    def onDestroy(self, *args):
        self.MainWindow.destroy()
        
    def swipe(self, left): # True means swiping left, False means swiping right
# Order lock - [home - agenda - traffic - news - mirror-screen]
        order = ['home', 'agenda', 'traffic', 'news', 'mirror-screen']
        cur_screen = self.stack.get_visible_child_name()
        if cur_screen == 'lock-screen':
            pygame.mixer.music.load('piano2.wav')
            pygame.mixer.music.play(0)
            self.go_to('home')
            return
        cur_ind = order.index(cur_screen)
        if left:
            if (cur_ind == 0): self.go_to('mirror-screen')
            else: self.go_to(order[cur_ind-1])
            self.ledstrip.left(0.001)
        else:
            if (cur_ind == len(order)-1): self.go_to('home')
            else: self.go_to(order[cur_ind+1])
            self.ledstrip.right(0.001)
        
    def go_to(self, screen):
        self.stack.set_visible_child_name(screen)

    
class MagicApp(Gtk.Application):
    def __init__(self, weatherObj, calendarObj, newsobject, detectorObj, ledstrip):
        Gtk.Application.__init__(self)
        self.weatherObject = weatherObj
        self.calendarObject = calendarObj
        self.newsObject = newsobject
        self.gestureDetector = detectorObj
        self.ledstrip = ledstrip

    def notes(self):        
        self.submit = self.win.GtkBuilder.get_object("submit")
        self.entry = self.win.GtkBuilder.get_object("entry")
        self.listbox = self.win.GtkBuilder.get_object("listbox")
        self.submit.connect("clicked", self.add_note) 
        self.delete = self.win.GtkBuilder.get_object("delete")
        self.delete.connect("clicked", self.delete_note)

    def do_activate(self):
        self.win = MagicWin(self, self.ledstrip)
        self.notes()
        self.update_time()                           # Update time on create
        self.update_weather()
        self.news()
        self.update_traffic()
        self.update_agenda()
        self.detect_gesture()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def update_time(self):
        labels = ['time-label', 'time-label1', 'time-label2', 'time-label3']
        time_labels = [self.win.GtkBuilder.get_object(l) for l in labels]
        for lab in time_labels:
            lab.set_text(datetime.datetime.now().strftime("%H:%M"))
        GLib.timeout_add(10000, self.update_time) # Update time every 10 sec
        
    def update_agenda(self):
        agenda_label_object = self.win.GtkBuilder.get_object('agenda_id')
        print(self.calendarObject.main())
        text = """Agenda for the day:
____________________________________________________
"""
        for item in self.calendarObject.main():
            time1 = datetime.datetime.strptime(item[0][0:18], "%Y-%m-%dT%H:%M:%S") # 2019-11-04T12:00:00+01:00
            time2 = datetime.datetime.strptime(item[1][0:18], "%Y-%m-%dT%H:%M:%S") # 2019-11-04T12:00:00+01:00
            text += "{} | {} - {} | {}\n".format(time1.strftime("%d-%m-%Y"), time1.strftime("%H:%M"), time2.strftime("%H:%M"), item[2])

        agenda_label_object.set_text(text)
        GLib.timeout_add(10000, self.update_agenda) # Update time every 10 sec

    def traffic_loop(self, datalist):
        dataver = datalist[1]
        datanum = datalist[0]
        countnum = datalist[2]
        traffic_all = self.win.GtkBuilder.get_object("traff")
        draad= dataver[countnum]
        traffic_all.set_text(draad)
        if countnum < datanum-1:
            countnum += 1
            datalist = [datanum, dataver, countnum]
            GLib.timeout_add(10000, self.traffic_loop, datalist)
        else:
            self.update_traffic()   


    def update_traffic(self): 
        abcd = Trafficcheck()
        dataver = abcd.Trafficimport()
        print(dataver)
        datanum = len(dataver)
        datalist= [datanum, dataver, 0]
        self.traffic_loop(datalist)

    def update_weather(self):
        self.weatherObject.update_weather()
        code = int(self.weatherObject.weather_id)
        filename = "gui/images/weather_icons/"
        if   200 <= code <= 299: filename += "thunder.png"
        elif 300 <= code <= 599: filename += "rain.png"
        elif 600 <= code <= 699: filename += "snow.png"
        elif 700 <= code <= 799: filename += "fog.png"
        elif        code == 800: filename += "clear.png"
        elif 801 <= code <= 804: filename += "clouds.png"

        weather_image_object = self.win.GtkBuilder.get_object('weather-icon')
        weather_image_object.set_from_file(filename)

        weather_label_object = self.win.GtkBuilder.get_object('weather-info')
        weather_label_object.set_text("""
        Weather in {}
        ______________________
        Description | {}
        Temperature | {} °C
        Wind        | {} km/h 
        """.format(
            self.weatherObject.location,
            self.weatherObject.weather_description,
            self.weatherObject.temp_current,
            self.weatherObject.wind_speed))
        GLib.timeout_add(600000, self.update_weather) # Update time every 600 sec

    def news(self):
        print("Calling function news")
        news_object = self.win.GtkBuilder.get_object('News_info')
        news_str = """"                                                                                 News for today
______________________________________________________________________________________________________________
"""
        news_list = self.newsObject.get_news()
        print("Getting news: ", len(news_list))
        for new in news_list:
            news_str += "{}\n{}\n\n".format(new[0],new[1])
            #news_str += "{}\n".format(new[0])
        news_object.set_text(news_str)
        GLib.timeout_add(100000, self.update_time)  # Update time every 100 sec
        
    def add_note(self, row): 
        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box()
        self.row.add(self.hbox)
        self.label = Gtk.Label(self.entry.get_text())
        self.hbox.pack_start(self.label, True, True, 0)
        self.listbox.add(self.row)
        self.listbox.show_all()

    def delete_note(self, row):
        row = self.listbox.get_selected_row()
        self.listbox.remove(row)
        
    def detect_gesture(self):
        self.gestureDetector.handle_image()
        if self.gestureDetector.status == 1: # Swipe left
            self.win.swipe(True)
        elif self.gestureDetector.status == 2: # Swipe right
            self.win.swipe(False)
        
        self.gestureDetector.status = 0
        GLib.timeout_add(1, self.detect_gesture) # while loop

if __name__ == "__main__":
    app = MagicApp()
    app.run(sys.argv)

