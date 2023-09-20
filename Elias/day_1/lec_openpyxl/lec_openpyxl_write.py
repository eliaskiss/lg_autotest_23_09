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
header = ['V1', 'V2', 'V3', 'V4', 'V5']
ws.append(header)
row = [10, 20, 30, 40, 50]
for i in range(10):
    ws.append(row)

############################################################
# Insert Datetime
############################################################
ws['A14'] = datetime.now()
ws['B14'] = datetime.now() + timedelta(days=1) # 내일
ws['C14'] = datetime.now() - timedelta(days=1) # 어제
ws['D14'] = datetime.now() + timedelta(hours=1) # 한시간뒤
ws['E14'] = '2023-04-12'

############################################################
# Merge/Unmerge Target Cell
############################################################
ws['A16'] = 'Hello'
ws['B16'] = 'World'

# Way I
# ws.merge_cells(range_string='A16:B16')
# ws.unmerge_cells('A16:B16')

# Way II
ws.merge_cells(start_row=16, start_column=1, end_row=16, end_column=2)
ws.unmerge_cells(start_row=16, start_column=1, end_row=16, end_column=2)

############################################################
# Insert Image
############################################################
img = Image('buz.jpg')
ws.add_image(img, 'G1')
























wb.save(file_name)



























