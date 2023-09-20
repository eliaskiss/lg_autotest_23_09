from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.drawing.image import Image
from datetime import datetime, timedelta

############################################################
# Create new excel workbook
############################################################
wb = Workbook()

file_name = './new_excel.xlsx'

############################################################
# Get Active Worksheet
############################################################
ws = wb.active

############################################################
# Set Sheet Name
############################################################
ws.title = 'Basic'

############################################################
# Set Cell Value
############################################################
ws['A1'] = 'Hello World'
ws['B1'] = 10
ws['C1'] = 20

############################################################
# Use formular
############################################################
ws['D1'] = '=SUM(B1+C1)'

############################################################
# Set Sheet Name
############################################################
comment = Comment('This is comment', 'Elias Kim', 100, 100)
ws['A1'].comment = comment

############################################################
# Insert Row
############################################################
ws['A8'] = 'Table Data'
header = ['V1', 'V2', 'V3', 'V4', 'V5']
ws.append(header)
row = [10, 20, 30, 40, 50]
for i in range(10):
    ws.append(row)

wb.save(file_name)



























