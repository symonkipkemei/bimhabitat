print("hello world")

import clr

clr.AddReference("RevitAPI")


import Autodesk

from Autodesk.Revit.DB import *

from pyrevit import forms

forms.alert()