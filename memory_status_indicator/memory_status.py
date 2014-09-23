#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import GLib
import os
import psutil
import json


class MemoryIndicator:
    def __init__(self):
        # General definitions
        self.attention = False
        self.MEGABYTE_DIVISOR = 1024 * 1024
        
        # Set user preferences
        self.user_conf = os.path.join(
            os.path.expanduser('~'),
            '.config/memory_status_indicator.conf'
        )
        try:
            self.show_label = json.load(open(self.user_conf))["show_label"]
        except:
            self.show_label = False
        
        # Set icons
        self.icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'icons/'
        ) 
        
        # Indicator instance      
        self.mem_indicator = appindicator.Indicator.new_with_path(
            "memory_indicator",
            "loading",
            appindicator.IndicatorCategory.SYSTEM_SERVICES,
            self.icon_path
        )
   
        # Define menu
        self.menu = Gtk.Menu()
        
        #title
        title = Gtk.MenuItem("Memory Status")
        title.set_state(Gtk.StateType.INSENSITIVE)
        self.menu.append(title)
        self.menu.append(Gtk.SeparatorMenuItem())
        #info
        self.menu_info_used = Gtk.MenuItem("Loading...")
        self.menu_info_used.set_state(Gtk.StateType.INSENSITIVE)
        self.menu.append(self.menu_info_used)
        #show label
        self.menu_conf_show_label = Gtk.CheckMenuItem("Show label")
        if self.show_label:
            self.menu_conf_show_label.set_active(True)
        self.menu_conf_show_label.connect("toggled", self.set_show_label)
        self.menu.append(self.menu_conf_show_label)
        
        self.menu.show_all()
        self.mem_indicator.set_menu(self.menu)
        self.mem_indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        

        self.total_memory_available = psutil.phymem_usage().total / self.MEGABYTE_DIVISOR
        
        # For each X seconds, the GLib loop call the get_memory_status method
        GLib.timeout_add(2000, self.get_memory_status)
        

    def get_memory_status(self):
        """ Method called every x times, definied by Gtk.timeout_add method
            This get memory information using psutil library and show in indicator.
        """

        memory_status = psutil.phymem_usage()

        self.menu_info_used.set_label("Memory used: %dMB / %dMB (%.1f%%)" % (
                memory_status.used / self.MEGABYTE_DIVISOR,
                self.total_memory_available, memory_status.percent
            )
        )

        round_percent_memory_available = int(round(memory_status.percent, -1))
        self.mem_indicator.set_icon("%d" % round_percent_memory_available)

        # Attention status if memory used is above 90
        if round_percent_memory_available >= 90 and not self.attention:
            self.mem_indicator.set_attention_icon("100")
            self.mem_indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
            self.attention = True
        elif round_percent_memory_available >= 90 and self.attention:
            self.mem_indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            self.attention = False

        # Set label if show_label is True
        if self.show_label:
            self.mem_indicator.set_label("%.1f%%" % memory_status.percent, "100%")

        # Return True for Gtk.timeout loop control
        return True

    def set_show_label(self, widget):
        if self.menu_conf_show_label.get_active():
            self.show_label = True
            with open(self.user_conf, 'w') as conf_file:
                conf_file.write('{"show_label": true}')
        else:
            self.show_label = False
            self.mem_indicator.set_label("", "100%")
            
            with open(self.user_conf, 'w') as conf_file:
                conf_file.write('{"show_label": false}')



if __name__ == "__main__":
    try:
        with open(r"/tmp/memory_status_indicator.pid", 'r') as pid_file:
            try:
                pid = int(pid_file.read())
                if not psutil.pid_exists(pid):
                    pid_file.seek(0)
                    pid_file.truncate()
                    pid_file.write(str(os.getpid()))
                else:
                    raise NameError("Memory Status Indicator already running")
            except ValueError:
                pid_file.seek(0)
                pid_file.write(str(os.getpid()))
                pid_file.truncate()
    except IOError:
        with open(r"/tmp/memory_status_indicator.pid", 'w') as pid_file:
            pid_file.write(str(os.getpid()))
  
    memory_indicator = MemoryIndicator()
    Gtk.main()