#-*- coding: utf-8 -*-

from Autodesk.Revit.DB import *

app      = __revit__.Application
rvt_year = int(app.VersionNumber)

def convert_Internal_to_m(length:int) -> float:
  """Convert internal units to meters

  Args:
      length (int): Length in internal revit units

  Returns:
      float: Length in meters rounded to 2 digits
  """
  rvt_year = int(app.VersionNumber)

  #if rvt < 22

  if rvt_year < 2022:
     return UnitUtils.Convert(length, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
    
  elif rvt_year > 2022:
     return UnitUtils.ConvertFromInternalUnits(length, DisplayUnitType.DUT_METERS)

