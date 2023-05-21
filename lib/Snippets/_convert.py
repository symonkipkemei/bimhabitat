#!python3
#-*- coding: utf-8 -*-


from Autodesk.Revit.DB import *

app      = __revit__.Application
doc      = __revit__.ActiveUIDocument.Document
rvt_year = int(app.VersionNumber)

def convert_Internal_to_m(length):
  """Convert internal units to meters

  Args:
      length (int): Length in internal revit units

  Returns:
      float: Length in meters rounded to 2 digits
  """
  rvt_year = int(app.VersionNumber)
  print (rvt_year)

  #if rvt < 22

  if rvt_year < 2022:
     return UnitUtils.Convert(length, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
    
  elif rvt_year >= 2022:
     return UnitUtils.ConvertFromInternalUnits(length, UnitTypeId.Meters)



if __name__ == "__main__":
    # Get all levels, they are constrained to read in feet, we are going to convert into mm
    all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

    for level in all_levels:
        print (level)

    print(convert_Internal_to_m(2000))