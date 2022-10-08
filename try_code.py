import pandas as pd
import openpyxl as pxl
import matplotlib.pyplot as plt

path_data = 'dataset/data_true.xlsx'
data = pxl.load_workbook(path_data)
sheet = data.sheetnames

dataset = pd.read_excel(path_data,
                        sheet_name=sheet[0])

chart_data = pd.melt(dataset, id_vars=["Provinsi"])
data = chart_data[chart_data["Provinsi"] == "Aceh"]
chart_data = data.loc[:, ["variable",
                          "value"]]
chart_data.set_index('variable', inplace=True)

chart_data.plot()
plt.show()