#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import numpy

def build_panorama(self,images):
    N = len(images)
    a = 20
    d=[0]

    small = pygame.surface.Surface((160,120),0,self.display)

    #Translate and print first Image
    arrays = [pygame.surfarray.array3d(images[0])]
    arrays[0] = numpy.asarray(arrays[0]).sum(axis = 2)
    small = pygame.transform.scale(images[0], (160,120), small)
    self.display.blit(small,(a,600))
    pygame.display.flip()

    #And now the rest
    for i in range(1,N):
        arrays.append(pygame.surfarray.array3d(images[i]))
        arrays[i] = numpy.asarray(arrays[i]).sum(axis = 2)
        d.append(determine_offset(arrays[i-1],arrays[i]))
        small = pygame.transform.scale(images[i], (160,120), small)
        a += (640-d[i])/4
        self.display.blit(small,(a,600))
        pygame.display.flip()

    final = pygame.surface.Surface(((a-20)*4+640,480),0,self.display)
    a=-640
    for i in range(N):
        a+=640-d[i]
        final.blit(images[i],(a,0))
    #a = 640
    #for i in range(1,N):
    #    images[i-1].set_alpha(127)
    #    final.blit(images[i-1],(a - d[i],0),(a - d[i],0,50,480))
    #    a+=640-d[i]
    #    images[i-1].set_alpha(None)
    return final


def determine_offset(a1, a2):
    (Y, X1) = a1.shape
    (Y, X2) = a2.shape
    maxoverlap = Y/2
    slicewidth = 100
    #pyramid = 4
    #sslicewidth = slicewidth/pyramid
    #sY = Y/pyramid
    ssd = []

    #sa1 = a1[::pyramid,::pyramid]
    #sa2 = a2[::pyramid,::pyramid]
    #for i in range(0,maxoverlap/pyramid):
    #    piece = numpy.subtract(sa1[sY-i-sslicewidth,:],sa2[0:sslicewidth,:])
    #    piece = numpy.multiply(piece,piece)
    #    ssd.append(piece.sum())
    #lowest = numpy.argmin(ssd)*pyramid
    #print lowest
    #ssd = []
    #for i in range(max(0,lowest-10),lowest+10):

    for i in range(0,maxoverlap):
        piece = numpy.subtract(a1[Y-i-slicewidth:Y-i,:],a2[0:slicewidth,:])
        piece = numpy.multiply(piece,piece)
        ssd.append(piece.sum())
    return numpy.argmin(ssd)+slicewidth
