#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
sys.path.insert(0, "lib")
import olpcgames
import pygame
from pygame import camera
from pygame.locals import *
import stitcher

log = logging.getLogger( 'Panorama run' )
log.setLevel( logging.ERROR )

class PanoCapture:
    def __init__(self, screen):
        self.size = ( 640, 480 )
        self.depth = 24
        self.thumbscale = 4
        self.display = pygame.display.set_mode( (1200,800), 0)
        self.display.fill((82, 186, 74))
        self.fuente = pygame.font.Font(None, 60)
        self.camlist = camera.list_cameras()
        self.camera = camera.Camera(self.camlist[0], self.size, "RGB")
        self.camera.start()
        self.camera.set_controls(True, False)
        self.clock = pygame.time.Clock()
        self.converted = pygame.surface.Surface(self.size, 0, self.display)
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)
        self.tiny = pygame.surface.Surface((self.size[0]/self.thumbscale,self.size[1]/self.thumbscale),0,self.display)
        self.final = None
        self.imlist = []
        self.offset = 20
        pygame.display.flip()
        #self.camera.set_controls(brightness = 129)

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

    def run(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.USEREVENT:
                    if hasattr(e,"action"):
                        if e.action == 'save_button':
                            self.show_text("Saving")
                            if not(self.imlist == []):
                                self.final = stitcher.build_panorama(self,self.imlist)
                            if self.final:
                                olpcgames.ACTIVITY.save_image(self.final)
                            pygame.display.flip()
                        elif e.action == 'new_button':
                            self.imlist = []
                            self.final = None
                            self.display.fill((82, 186, 74))
                            self.offset = 20
                            pygame.display.flip()
                        elif e.action == 'capture_button':
                            self.imlist.append(self.snapshot.copy())
                            self.display.blit(self.snapshot, (20,0))
                            self.tiny = pygame.transform.scale(self.snapshot, (self.size[0]/self.thumbscale,self.size[1]/self.thumbscale), self.tiny)
                            self.display.blit(self.tiny,(self.offset,480))
                            self.offset += 3*self.size[0]/(4*self.thumbscale)
                            pygame.display.flip()
                        elif e.action == 'stitch_button':
                            self.show_text("Processing")
                            if not(self.imlist == []):
                                self.final = stitcher.build_panorama(self,self.imlist)
                            pygame.display.flip()
                elif e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    going = False
                elif e.type == KEYDOWN and e.key == K_SPACE:
                    self.imlist.append(self.snapshot.copy())
                    self.display.blit(self.snapshot, (20,0))
                    self.tiny = pygame.transform.scale(self.snapshot, (self.size[0]/self.thumbscale,self.size[1]/self.thumbscale), self.tiny)
                    self.display.blit(self.tiny,(self.offset,480))
                    self.offset += 3*self.size[0]/(4*self.thumbscale)
                    pygame.display.flip()

            self.get_and_flip()
            self.clock.tick()
            #print self.clock.get_fps()


def main():
    toolbarheight = 75
    tabheight = 45
    pygame.init()
    camera.init()
    pygame.display.init()
    x,y  = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((x,y-toolbarheight-tabheight))
    # create an instance of the game
    cap = PanoCapture(screen)
    # start the main loop
    cap.run()

# make sure that main get's called
if __name__ == '__main__':
    main()
