import pandas as pd
import numpy as np

path_data = 'dataset/data_true.xlsx'

dataset = pd.read_excel(path_data,
                        sheet_name="Cakupan_JKN")

bar_data = pd.melt(dataset, id_vars=["Provinsi"])

print(bar_data)