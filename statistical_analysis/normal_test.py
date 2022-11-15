import xlrd
from scipy import stats

# MyListening,2048,HuaWei,HuJiang,TravelDiary,Wonderland

project = 'Wonderland'
ExcelPath = 'E:/result/APFDs/' + project + '.xls'
workbook = xlrd.open_workbook(ExcelPath)
sheet1 = workbook.sheet_by_name(project)
nrows = sheet1.nrows  # 30 rows
ncolumns = 5  # 5 columns

RANDOM = []
BDDiv = []
DMBD19 = []
TSE20 = []
CTRP = []

for row in range(1, nrows):
    RANDOM.append(sheet1.cell_value(row, 0))
for row in range(1, nrows):
    BDDiv.append(sheet1.cell_value(row, 1))
for row in range(1, nrows):
    DMBD19.append(sheet1.cell_value(row, 2))
for row in range(1, nrows):
    TSE20.append(sheet1.cell_value(row, 3))
for row in range(1, nrows):
    CTRP.append(sheet1.cell_value(row, 4))

print('RANDOM', RANDOM)
print('BDDiv', BDDiv)
print('DMBD19', DMBD19)
print('TSE20', TSE20)
print('CTRP', CTRP)

print(stats.shapiro(RANDOM))
print(stats.shapiro(BDDiv))
print(stats.shapiro(DMBD19))
print(stats.shapiro(TSE20))
print(stats.shapiro(CTRP))
