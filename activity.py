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
import gtk
import pygame
import sugargame
import sugargame.canvas
from sugar.activity import activity
from sugar.datastore import datastore
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbutton import ToolButton

from gettext import gettext as _

import pano

class PanoramaActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.auto_stich = False
        self.actividad = pano.PanoCapture(self)

        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.run_pygame(self.actividad.run)

    def build_toolbar(self):

        self.max_participants = 1

        toolbox = ToolbarBox()
        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        pano_toolbar = toolbox.toolbar

        new_button = ToolButton('stock_refresh')
        new_button.set_tooltip(_('New Panorama'))
        new_button.connect('clicked', self.new_event)
        pano_toolbar.insert(new_button, -1)
        new_button.show()

        capture_button = ToolButton('add_capture')
        capture_button.set_tooltip(_('Add a capture to the Panorama'))
        capture_button.connect('clicked', self.capture_event)
        pano_toolbar.insert(capture_button, -1)
        capture_button.show()

        stitch_button = ToolButton('format-columns-triple')
        stitch_button.set_tooltip(_('Stitch Panorama'))
        stitch_button.connect('clicked', self.stitch_event)
        pano_toolbar.insert(stitch_button, -1)
        stitch_button.show()

        stiching_auto = ToolButton('media-playback-start')
        stiching_auto.set_tooltip(_('Enable auto-stitch'))
        stiching_auto.connect('clicked', self.change_stich)
        pano_toolbar.insert(stiching_auto, -1)

        save_button = ToolButton('filesave')
        save_button.set_tooltip(_('Save Panorama'))
        save_button.connect('clicked', self.save_event)
        pano_toolbar.insert(save_button, -1)
        save_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        pano_toolbar.insert(separator,-1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = '<Ctrl>q'
        pano_toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbox)

        toolbox.show_all()

    def save_image(self,image):
        journalobj = datastore.create()
        journalobj.metadata['title'] = _('Panorama')
        journalobj.metadata['mime_type'] = 'image/jpeg'

        file_path = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'], 'data', 'panorama.jpg')

        pygame.image.save(image,file_path)
        journalobj.set_file_path(file_path)
        datastore.write(journalobj)

        journalobj.destroy()

    def change_stich(self, options):
        self.auto_stich = not self.auto_stich
        self.actividad.auto_stiching(self.auto_stich)
        if self.auto_stich:
            options.set_icon('media-playback-stop')
            options.set_tooltip(_('Disable auto-stitch'))
        else:
            options.set_icon('media-playback-start')
            options.set_tooltip(_('Enable auto-stitch'))

    def save_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='save_button'))

    def new_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='new_button'))

    def capture_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='capture_button'))

    def stitch_event(self,widget):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='stitch_button'))


class Combo(gtk.ComboBox):

    def __init__(self, options):

        self.liststore = gtk.ListStore(str)

        for o in options:
            self.liststore.append([o])

        gtk.ComboBox.__init__(self, self.liststore)

        cell = gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)

        self.set_active(0)

