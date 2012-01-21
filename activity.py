#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import os
import sys
sys.path.insert(0, "lib")
import olpcgames
import pygame
import stitcher

# Load sugar libraries
from sugar.activity import activity
from sugar.datastore import datastore
from sugar.graphics.toolbutton import ToolButton

class PanoramaActivity(olpcgames.PyGameActivity):

    game_name = 'pano'
    game_title = 'Panorama'
    game_size = None

    def build_toolbar(self):
        # make a toolbox
        toolbox = activity.ActivityToolbox(self)

        # modify the Activity tab
        activity_toolbar = toolbox.get_activity_toolbar()

        # remove keep and share buttons
        activity_toolbar.remove(activity_toolbar.keep)
        activity_toolbar.keep = None
        activity_toolbar.remove(activity_toolbar.share)
        activity_toolbar.share = None
        self.blocklist = []
        # make a 'pano' toolbar
        pano_toolbar = gtk.Toolbar()

        new_button = ToolButton('stock_refresh')
        new_button.set_tooltip("New Panorama")
        new_button.connect('clicked', self.new_event)
        pano_toolbar.insert(new_button, -1)
        new_button.show()

        capture_button = ToolButton('add_capture')
        capture_button.set_tooltip("Add a capture to the Panorama")
        capture_button.connect('clicked', self.capture_event)
        pano_toolbar.insert(capture_button, -1)
        capture_button.show()

        stitch_button = ToolButton('format-columns-triple')
        stitch_button.set_tooltip("Stitch Panorama")
        stitch_button.connect('clicked', self.stitch_event)
        pano_toolbar.insert(stitch_button, -1)
        stitch_button.show()

        save_button = ToolButton('filesave')
        save_button.set_tooltip("Save Panorama")
        save_button.connect('clicked', self.save_event)
        pano_toolbar.insert(save_button, -1)
        save_button.show()

        # add the toolbars to the toolbox
        toolbox.add_toolbar("Panoramas",pano_toolbar)
        pano_toolbar.show()
        toolbox.show()
        self.set_toolbox(toolbox)
        toolbox.set_current_toolbar(1)
        return activity_toolbar


    def save_image(self,image):
        journalobj = datastore.create()
        journalobj.metadata['title'] = 'Panorama'
        journalobj.metadata['mime_type'] = 'image/jpeg'

        file_path = os.path.join(olpcgames.ACTIVITY.get_activity_root(),'instance','panorama.jpg')

        pygame.image.save(image,file_path)
        journalobj.set_file_path(file_path)
        datastore.write(journalobj)

        journalobj.destroy()

    def save_event(self,widget):
        pygame.event.post(olpcgames.eventwrap.Event(pygame.USEREVENT, action='save_button'))

    def new_event(self,widget):
        pygame.event.post(olpcgames.eventwrap.Event(pygame.USEREVENT, action='new_button'))

    def capture_event(self,widget):
        pygame.event.post(olpcgames.eventwrap.Event(pygame.USEREVENT, action='capture_button'))

    def stitch_event(self,widget):
        pygame.event.post(olpcgames.eventwrap.Event(pygame.USEREVENT, action='stitch_button'))
