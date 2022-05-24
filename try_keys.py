#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:02:53 2021

@author: skoczen
"""

import os, sys, platform
import tty, termios

def _GetchUnix():
    fd = sys.stdin.fileno()
    #print(fd)
    old_settings = termios.tcgetattr(fd)
    try:
        #tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def clear_n_lines(n):
	clr='\033[%dA'%n
	for i in range(n):
		clr+='\033[2K\n'
	clr+='\033[%dA'%(n+1)
	print(clr)
    
getch=_GetchUnix()
clear_n_lines(20)
        
print(getch)       
 