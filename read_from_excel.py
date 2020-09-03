import xlrd

loc = 'stand_stats.xlsx'
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
rows = sheet.nrows
cols = sheet.ncols
stand_stats = [[0] * cols] * rows
print(stand_stats)
i = 0
while i < rows:
    j = 0
    while j < cols:
        stand_stats[i][j] = sheet.cell_value(i,j)
        j = j + 1
    i = i + 1
print(stand_stats)