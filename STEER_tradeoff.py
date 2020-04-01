import pandas as pd
import numpy as np

from pandas import ExcelWriter
from pandas import ExcelFile

from pathlib import Path



file_name = 'new_one.xlsx'
#file_name = 'code_test.xlsx'


#change names for input, impact and ouput matrices and respective sheet names
file_name = 'new_one.xlsx'
sheet_name_input = 'input'
matrix_number = 1
sheet_name_impact = 'impact' + str(matrix_number)
output_name = 'trade_off' + str(matrix_number)


excel_output_name = output_name + '.xlsx'
sheet_name_output = output_name + '_sheet'

df_input = pd.read_excel(file_name, sheet_name = sheet_name_input)
df_impact = pd.read_excel(file_name, sheet_name = sheet_name_impact)

df_input = df_input.replace(np.nan, '0', regex=True)
df_impact = df_impact.replace(np.nan, '0', regex=True)


# create trade_off matrix
ESI_list = []
for i in range(1, len(df_input.columns)):
    ESI_list.append('ESI\n' + str(i))

df_tradeoff = pd.DataFrame(index=ESI_list , columns=ESI_list)

input_list = []
# interate as often as there are columns in the input table (-1)
for i in range(1, len(df_input.columns)):

    # get all inputs listed
    input_list = df_input[list(df_input.columns.values.tolist())[i]].values.tolist()

    counter = 0
    changed = False

    # in respect to the input table, iterate over the impact table and create the trade_off matrix
    for l in range(1, len(df_input.columns)):
        for k in range(1, len(input_list) + 1):
            if input_list[k - 1] == '+':
                value = df_impact.iat[l-1, k]

                if value == '0' or value == 0:
                    pass
                elif value == '+':
                    counter += 1
                    changed = True
                elif value == '-':
                    counter += -1
                    changed = True
                else:
                    print('something is wrong in the impact table, no data found')

        if counter == 0 and changed:
            df_tradeoff.iat[l-1, i-1] = '+/-'
        elif counter == 0 and not changed:
            df_tradeoff.iat[l-1, i-1] = ' '
        elif counter > 0:
            df_tradeoff.iat[l-1, i-1] = '+'
        elif counter < 0:
            df_tradeoff.iat[l-1, i-1] = '-'
        else:
            print('the counter didn\'t work')

        counter = 0
        changed = False

print(df_tradeoff)


writer = pd.ExcelWriter(excel_output_name)
df_tradeoff.to_excel(writer, sheet_name_output)
writer.save()
print('DataFrame is written successfully to Excel File.')
