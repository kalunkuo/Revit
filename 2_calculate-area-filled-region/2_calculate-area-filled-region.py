__author__ = "karen.kuo"
__version__ = "2024.03.21"

"""
Program: Dynamo + Revit

Description:
The script adds up areas based on the program and name. 
It then returns a list of total areas for each combination of program and name.

Input:
1. data_area: Contains areas to be added up.
2. data_program: Contains program names.
3. data_name: Contains corresponding names.

Output: list of total areas for each combination
"""

# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Unpack input data
data_area = IN[0]
data_program = IN[1]
data_name = IN[2]

# Create a dictionary to store areas corresponding to program and name
area_dict = {}

for area, program, name in zip(data_area, data_program, data_name):
    key = (program, name)
    if key in area_dict:
        area_dict[key] += float(area)
    else:
        area_dict[key] = float(area)

# Convert the dictionary back to a list of tuples
list_result = area_dict.items()

# Example usage:
print("list_result: ", len(result), result[0][0] , result)

list_sum_area = []

for i in range(len(data_name)):
	for j in range(len(result)):
		if data_program[i] == list_result[j][0][0] and data_name[i] == list_result[j][0][1]:
			list_sum_area.append(list_result[j][1])

# Example usage:
print("list_sum_area: ", list_sum_area[0])

OUT = list_sum_area
