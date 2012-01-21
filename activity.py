#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Panorama
# Copyright (C) 2008, Nirav Patel
# Copyright (C) 2011, 2012, Alan Aguiar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar <alanjas@gmail.com>
# Nirav Patel <sugarlabs@spongezone.net>

import os
import sys
import gtk
sys.path.insert(0, "lib")
import pygame
import stitcher
import sugargame
import sugargame.canvas
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
from sugar.datastore import datastore
from sugar.graphics.toolbutton import ToolButton
from gettext import gettext as _

import pano

class PanoramaActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.actividad = pano.PanoCapture(self)

        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.run_pygame(self.actividad.run)

    def build_toolbar(self):

        caja = activity.ActivityToolbox(self)

        toolbar = caja.get_activity_toolbar()
        toolbar.remove(toolbar.keep)
        toolbar.keep = None
        toolbar.remove(toolbar.share)
        toolbar.share = None


        #self.blocklist = []

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


        caja.add_toolbar("Panoramas", pano_toolbar)
        pano_toolbar.show()
        #caja.show()
        #self.set_toolbox(toolbox)

        caja.show_all()
        self.set_toolbox(caja)

        # que hace esto

        caja.set_current_toolbar(1)


    def save_image(self,image):
        journalobj = datastore.create()
        journalobj.metadata['title'] = 'Panorama'
        journalobj.metadata['mime_type'] = 'image/jpeg'

        #file_path = os.path.join(olpcgames.ACTIVITY.get_activity_root(),'instance','panorama.jpg')

        file_path = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'], 'data', 'panorama.jpg')

        pygame.image.save(image,file_path)
        journalobj.set_file_path(file_path)
        datastore.write(journalobj)

        journalobj.destroy()

    def save_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='save_button'))

    def new_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='new_button'))

    def capture_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='capture_button'))

    def stitch_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='stitch_button'))
