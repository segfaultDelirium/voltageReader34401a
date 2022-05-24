#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:14:13 2021

@author: skoczen
"""

var = input("Please enter something: ")
print("You entered: " + var)
print(type(var))
if var.isdigit():
    print("Is didgit")
