#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appindicator
import gtk
import os


class MemoryIndicator:
    def __init__(self):
        # Set icons
        self.icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'icons/'
        ) 
        
        # Indicator instance      
        self.mem_indicator = appindicator.Indicator(
            "memory_indicator",
            "loading",
            appindicator.CATEGORY_APPLICATION_STATUS,
            self.icon_path
        )
   
   # Define menu
        self.menu = gtk.Menu()

        title = gtk.MenuItem("Memory Status")
        title.set_state(gtk.STATE_INSENSITIVE)
        self.menu.append(title)
        self.menu.append(gtk.SeparatorMenuItem())
        self.menu_info_used = gtk.MenuItem("Loading...")
        self.menu_info_used.set_state(gtk.STATE_INSENSITIVE)
        self.menu.append(self.menu_info_used)
        self.menu.show_all()
        self.mem_indicator.set_menu(self.menu)
        self.mem_indicator.set_status(appindicator.STATUS_ACTIVE)


if __name__ == "__main__":
    memory_indicator = MemoryIndicator()
    gtk.main()