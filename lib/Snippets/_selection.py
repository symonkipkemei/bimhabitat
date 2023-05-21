#-*- coding: utf-8 -*-

#imports

from Autodesk.Revit.DB import *

#variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


def get_selected_elements(uidoc):
    """select objects that represent the current active environment
            :param uidoc: access to an object in revit environ
            :return: selected elements
            """

    selected_elements = []
    for element_id in uidoc.Selection.GetElementIds():
        elem = uidoc.Document.GetElement(element_id)
        selected_elements.append(elem)

    return selected_elements


if __name__ == "__main__":
    print (get_selected_elements(uidoc))

