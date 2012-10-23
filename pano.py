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
import time
import logging
import stitcher
try:
    import pygame
    from pygame.locals import *
    from pygame import camera
except ImportError:
    print 'Error in import Pygame. This activity requires Pygame 1.9'


class PanoCapture():

    def __init__(self, parent):
        self.parent = parent
        self.auto_stich = False

        #self.camera.set_controls(brightness = 129)

    def auto_stiching(self, option):
        self.auto_stich = option

    def show_text(self,texto):
        text = self.fuente.render(texto, 1, (255,0,0))
        textrect = text.get_rect()
        textrect.center = (820, 240)
        self.display.blit(text, textrect)
        pygame.display.flip()

    def get_and_flip(self):
        self.snapshot = self.camera.get_image(self.snapshot)
        #box = self.display.blit(self.snapshot, (500,0))
        #pygame.display.update(box)
        self.display.blit(self.snapshot, (500,0))
        pygame.display.flip()

    def add_capture(self):
        N = len(self.imlist)
        if not(N == self.max_cant):
            self.imlist.append(self.snapshot.copy())
            self.display.blit(self.snapshot, (20,0))
            self.tiny = pygame.transform.scale(self.snapshot, (self.size[0]/self.thumbscale,self.size[1]/self.thumbscale), self.tiny)
            self.display.blit(self.tiny,(self.offset,480))
            self.offset += 3*self.size[0]/(4*self.thumbscale)
            pygame.display.flip()
        else:
            self.show_text('Max cant of captures')

    def run(self):
        self.size = (640, 480)
        self.depth = 24
        self.thumbscale = 4
        pygame.init()
        pygame.camera.init()
        self.fuente = pygame.font.Font(None, 60)
        self.camlist = camera.list_cameras()
        self.camera = camera.Camera(self.camlist[0], self.size, "RGB")
        self.camera.set_controls(True, False)
        self.camera.start()
        self.clock = pygame.time.Clock()
        self.final = None
        self.imlist = []
        self.offset = 20
        self.max_cant = 9
        self.display = pygame.display.get_surface()
        self.display.fill((82, 186, 74))

        self.converted = pygame.surface.Surface(self.size, 0, self.display)
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)
        self.tiny = pygame.surface.Surface((self.size[0]/self.thumbscale,self.size[1]/self.thumbscale),0,self.display)
        pygame.display.flip()

        going = True
        while going:
            #GTK events
            while gtk.events_pending():
                gtk.main_iteration()

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.USEREVENT:
                    if hasattr(e,"action"):
                        if e.action == 'save_button':
                            self.show_text("Saving")
                            if self.final:
                                self.parent.save_image(self.final)
                            else:
                                if not(self.imlist == []):
                                    self.final = stitcher.build_panorama(self, self.imlist, self.auto_stich)
                                    self.parent.save_image(self.final)
                            pygame.display.flip()
                        elif e.action == 'new_button':
                            self.imlist = []
                            self.final = None
                            self.display.fill((82, 186, 74))
                            self.offset = 20
                            pygame.display.flip()
                        elif e.action == 'capture_button':
                            self.add_capture()
                        elif e.action == 'stitch_button':
                            self.show_text("Processing")
                            if not(self.imlist == []):
                                self.final = stitcher.build_panorama(self, self.imlist, self.auto_stich)
                            pygame.display.flip()
                elif e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    going = False
                elif e.type == KEYDOWN and e.key == K_SPACE:
                    self.add_capture()


            self.get_and_flip()
            self.clock.tick()

        if self.camera:
            self.camera.stop()
        

