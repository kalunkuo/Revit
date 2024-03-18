__author__ = "karen.kuo"
__version__ = "2024.03.04"

# Importing necessary modules
import rhinoscriptsyntax as rs
import clr
import os

# Adding references
clr.AddReference("RhinoInside.Revit")
clr.AddReference('System.Core')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
clr.AddReference("RevitServices")
clr.AddReference("RhinoCommon")

# Importing Rhino modules
import Rhino.Geometry as rg
import ghpythonlib.components as gh

# Importing Rhino.Inside modules
from RhinoInside.Revit import Revit
from RhinoInside.Revit.Convert import Geometry

# Importing Revit API modules
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import UIApplication
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Importing Revit filters and utilities
from Autodesk.Revit.DB import (FilteredElementCollector, BuiltInCategory, ElementLevelFilter)

# Importing System collections
from System.Collections.Generic import List

# Importing math module
import math

# Retrieving active application and document
app = Revit.ActiveUIApplication.Application
doc = Revit.ActiveUIDocument.Document

# Function to find duplicate indices in a list of geometries
def find_duplicates_indices(geometries):
    duplicates = []
    for i in range(len(geometries)):
        for j in range(i + 1, len(geometries)):
            if rg.GeometryBase.GeometryEquals(geometries[i], geometries[j]):
                duplicates.append(j)
    return duplicates

# Retrieving level and annotation lines
level = None
list_lines_revit = []
list_lines_rhino = []

# Duplicate level detection
level_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()
for l in level_collector:
    if l.Id == IN_level.Id:
        level = l

if IN_boo and level:
    level_name = IN_level.Name
    level_filter = ElementLevelFilter(level.Id)
    detail_lines_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType().ToElements()
    
    for model_line in detail_lines_collector:
        if model_line.SketchPlane.Name == level_name:
            list_lines_revit.append(model_line)
            line = model_line.GeometryCurve
            line_rhino = line.ToCurve()
            list_lines_rhino.append(line_rhino)
    
    list_lines_rhino_copy = list(list_lines_rhino)
    duplicates_indices = find_duplicates_indices(list_lines_rhino_copy)
    
    while duplicates_indices:
        t = Transaction(doc, "Delete Duplicates")
        try: 
            t.Start()
            for index in sorted(duplicates_indices, reverse=True):
                del list_lines_rhino_copy[index]
                doc.Delete(list_lines_revit[index].Id)
            t.Commit()
        except Exception as e:
            t.RollBack()
            print("An error occurred during the transaction:", str(e))
        
        duplicates_indices = find_duplicates_indices(list_lines_rhino_copy)

OUT_list_lines_revit = list_lines_revit
