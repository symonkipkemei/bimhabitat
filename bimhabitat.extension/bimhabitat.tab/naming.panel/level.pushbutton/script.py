# we have to first specify that the encoding comes from PEP0236, a format understood by revit

#-*- coding: utf-8 -*-



# we will follow by filling in the metadata

__title__ = "Elevation pad"


__doc__ = """ Version  1.1
Date  = 19.05.2023
___________________________________________________________________________
Description:

This tool will update your level name to include the elevation height

___________________________________________________________________________
How-to:

-> Click on the button
-> Change settings optional
-> Rename levels

___________________________________________________________________________
last update:
- [19.05.2023] - 1.0 RELEASE

___________________________________________________________________________
To-Do:
___________________________________________________________________________
Author: Symon Kipkemei

"""


__author__ = "Symon Kipkemei"
__helpurl__ = "https://www.linkedin.com/in/symon-kipkemei/"

__highlight__ = 'new'

__min_revit_ver__= 2020
__max_revit_ver__ = 2022




#imports to keep the code running

""" __ ___  ___ ____    ___   ____  ______  __ 
 || ||\\//|| || \\  // \\  || \\ | || | (( \
 || || \/ || ||_// ((   )) ||_//   ||    \\ 
 || ||    || ||     \\_//  || \\   ||   \_))
                                            
"""
################################################################

#regular
import math, os, sys,datetime, time
from pprint import pprint
#Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction, Element, ElementId, FilteredElementCollector

# pyrevit
from pyrevit import revit,forms

# custom imports (from our native library)
#from libi.snippets._selection import get_selected_elements
from libi.snippets._convert import convert_Internal_to_m


#.NET imports ( I have no idea why I am importing this)
import clr
clr.AddReference("System")
from System.Collections.Generic import List #List<ElementType>() <-it's special type of list that RevitAPI often requires


"""
 __ __  ___  ____  __  ___  ____  __     ____  __ 
 || || // \\ || \\ || // \\ || )) ||    ||    (( \
 \\ // ||=|| ||_// || ||=|| ||=)  ||    ||==   \\ 
  \V/  || || || \\ || || || ||_)) ||__| ||___ \_))
                                                  
"""

################################################################
#Variables ( variables should be abstracted from __revit__)


doc    = __revit__.ActiveUIDocumnet.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
PATH_SCRIPT = os.path.dirname(__file__)

symbol_start = "["
symbol_end = "]"


#FUNCTION AND CLASSES

"""
  ____ __ __ __  __   ___ ______ __   ___   __  __  __ 
 ||    || || ||\ ||  //   | || | ||  // \\  ||\ || (( \
 ||==  || || ||\\|| ((      ||   || ((   )) ||\\||  \\ 
 ||    \\_// || \||  \\__   ||   ||  \\_//  || \|| \_))
                                                       
"""
################################################################




# Get all levels, they are constrained to read in feet, we are going to convert into mm

all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
pprint(all_levels)
# Determine elevation heights

for lvl in all_levels:
    lvl_elevation = lvl.Elevation
    lvl_elevation_m = round(convert_Internal_to_m(lvl_elevation), 2)
    lvl_elevation_m_str = "+" + str(lvl_elevation_m) if lvl_elevation > 0 else str(lvl_elevation_m)



#TODO ELEVATION EXISTS (update)


# Elevation does not exist(new)
elevation_value = symbol_start + lvl_elevation_m_str + symbol_end
new_name = lvl.Name + elevation_value


#run the changes
t = Transaction(doc, __title__)
t.Start()
try:
    lvl.Name = new_name
except:
    print("Could not change level's name")

t.commit
    


