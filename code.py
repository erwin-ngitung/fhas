import json
import numpy as np

f = open('dataset/data_email.json')

data_email = json.load(f)

index = np.where(np.array(data_email['email']) == 'fhas.developer@gmail.com')

print(index[0][0])