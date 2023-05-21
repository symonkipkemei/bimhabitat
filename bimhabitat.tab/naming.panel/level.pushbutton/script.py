#-*- coding: utf-8 -*-
# we have to first specify that the encoding comes from PEP0236, a format understood by revit



"""METADATA DOCUMENTATION"""
###########################################################

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
- [21.05.2023] - 1.1 RELEASE

___________________________________________________________________________
To-Do:
-> Integrate mode for suffix/prefix
-> Integrate mode for remove elevation mark

___________________________________________________________________________
Author: Symon Kipkemei

"""


__author__ = "Symon Kipkemei"
__helpurl__ = "https://www.linkedin.com/in/symon-kipkemei/"

__highlight__ = 'new'

__min_revit_ver__= 2020
__max_revit_ver__ = 2022



"""IMPORTS"""
################################################################

#regular
import os
from pprint import pprint
#Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction, FilteredElementCollector

# importing from our lib package does not work, pyRevit claims there is a an Module not found error
# we will therefore creating functions innately in this script and not as a package

#CUSTOM IMPORTS
#from lib.Snippets import _convert

#.NET imports ( I have no idea why I am importing this)

import clr
clr.AddReference("System")

"""VARIABLES"""
################################################################

#Variables ( variables should be abstracted from __revit__)

app      = __revit__.Application
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument


PATH_SCRIPT = os.path.dirname(__file__)

symbol_start = "("
symbol_end = ")"


"""FUNCTION AND CLASSES"""
################################################################

def reset_default_name(text,symbol_start,symbol_stop):
    # type:(str,str,str) -> str
    """
    Reset the original name by deleting the elevation name
    :param text: the current elevation name
    :param symbol_start: start symbol
    :param symbol_stop: stop symbol
    :return: The default name
    """

    index_start = text.find(symbol_start)
    index_stop = text.find(symbol_stop) + 1

    elevation = text[index_start:index_stop]
    print(elevation)

    default_name = text.replace(elevation,"")

    return  default_name





def get_text_in_brackets(text, symbol_start,symbol_end):
    #type:(str,str,str) -> str
    """Get content between two brackets
    :param text: the entire text
    :param symbol_start: start symbol
    :param symbol_end: end symbol
    :return: Text between two symbols
    """

    if symbol_start in text and symbol_end in text:
        start_symbol_index = text.find(symbol_start) + len(symbol_start)  #
        stop_symbol_index = text.find(symbol_end)
        return text[start_symbol_index:stop_symbol_index]

    #if none return empty string
    return ""


def suffix_placement(default_name, elevation_name, suffix = True):
    #type:(str,str,bool) -> str
    """Detemine placement of elevation name , suffix or prefix

    :param default_name: The default level name (lvl.Name)
    :param elevation_name: The elvation difference in m i.e (+6.1)
    :param suffix: If True the elevation is placed at suffix if false the reverse is true
    :return: the new name
    """

    if suffix == True:
        text = default_name + elevation_name
    else:
        text = elevation_name + default_name
    return  text

def convert_Internal_to_m(length):
    """Convert internal units to meters

    Args:
        length (int): Length in internal revit units

    Returns:
        float: Length in meters rounded to 2 digits
    """
    rvt_year = int(app.VersionNumber)
    # if rvt < 22

    if rvt_year < 2022:
        return UnitUtils.Convert(length, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)

    elif rvt_year >= 2022:
        return UnitUtils.ConvertFromInternalUnits(length, UnitTypeId.Meters)


# Get all levels, they are constrained to read in feet, we are going to convert into mm

all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

# Determine elevation heights

#run the changes
t = Transaction(doc, __title__)
t.Start()

for lvl in all_levels:
    #once we retrieve the object we can retrieve the attributes/members associated with the object such elevation ( to establish this use revit look up)
    lvl_elevation = lvl.Elevation
    lvl_elevation_m = round(convert_Internal_to_m(lvl_elevation), 2)
    lvl_elevation_m_str = "+" + str(lvl_elevation_m) if lvl_elevation > 0 else str(lvl_elevation_m)

    #if elevation name already exists , update the values
    if symbol_start in lvl.Name and symbol_end in lvl.Name:
        current_value = get_text_in_brackets(lvl.Name, symbol_start, symbol_end)
        new_name = lvl.Name.replace(current_value,lvl_elevation_m_str)

    else:
        # Elevation extension to the name
        elevation_value = symbol_start + lvl_elevation_m_str + symbol_end
        new_name = lvl.Name + elevation_value

    try:
        current_name = lvl.Name
        lvl.Name = new_name
        print ("Renamed: {} -> {}".format(current_name, new_name))
    except Exception as e:
        print("Could not change level's name,due to error :  {}".format(e))



t.Commit()

print ("_"*50)
print ("The script is finished")


if __name__ == "__main__":
    reset_default_name("roof(+6.1)", "(",")")



