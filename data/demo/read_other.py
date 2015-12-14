# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 17:38:44 2015

@author: Alexis
"""
import os
import pandas as pd
import numpy as np


## lecture brute
## lecture brute
path = "D:\\data\\Taxi"
file_path = os.path.join(path, 'extract_patrouilles_janvier.csv')

tab = pd.read_csv(file_path, sep=';')


# 46

## .pas besoin de garder name, qui redit ident
#assert max(tab.groupby('IDENT')['NAME'].nunique()) == 1
#assert max(tab.groupby('NAME')['IDENT'].nunique()) == 1
#passage_ident_name = tab.groupby('NAME')['IDENT'].unique()
del tab['NAME']

print("il y a ", len(tab), ' valeurs initialement et ', 
      len(tab.drop_duplicates()), ' sans doublons'
      )
          
tab.drop_duplicates(inplace=True)
tab.X = tab.X.str.replace(',','.').astype(float)
tab.Y = tab.Y.str.replace(',','.').astype(float)

print(tab.X.astype(int).value_counts())
print(tab.Y.astype(int).value_counts())

tab[tab.Y > 53]
tab[tab.Y > 53].IDENT.value_counts()
# il y a un bug? Réparti sur tous

list_vehicule = tab.IDENT.unique()

# il faut traiter véhicule par véhicule
vehicule1 = list_vehicule[0]
tab_1 = tab[tab.IDENT == vehicule1]


# faire la carte :
## centre
center_X = tab.X.mean()
center_Y = tab.Y.mean()


test = tab.loc[tab.DATE < '2014-01-20']
# transform to json 
test.rename(columns={
    'DATE': 'timestamp_1',
    'IDENT':'id',
    'X': 'longitude',
    'Y': 'latitude',
    }, inplace=True)


test['timestamp'] = pd.to_datetime(test.timestamp_1).astype(np.int64)
test['timestamp'] = (test['timestamp']/1e6).astype(np.int64)
#del test['timestamp_1']
test.to_csv('extract.csv', index=False)