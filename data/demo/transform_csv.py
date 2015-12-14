# -*- coding: utf-8 -*-
import os
import csv
import pandas as pd

script_dir = os.path.realpath(os.path.dirname(__file__))

csv_file_path = os.path.join(script_dir, 'data', 'extract.csv')
tab = pd.read_csv(csv_file_path)

init_js =  ''' "type": "Feature",
    "geometry": {
    "type": "MultiPoint",
    "coordinates": [
'''

intermediate_js = '''   ]
  },
  "properties": {
    "time": [
'''

def check_table(tab):
    if len(tab) == 1:
        return True
    tab['delta'] = tab['timestamp'] - tab['timestamp'].shift(1)
    # deplacement
    tab['diff_lat'] = tab['latitude'] - tab['latitude'].shift(1)
    tab['diff_lon'] = tab['longitude'] - tab['longitude'].shift(1) 
    assert tab['delta'].min() > 0
    immobile = (tab['diff_lat'] == 0) & (tab['diff_lon'] == 0)
    assert not any(immobile)
    return True


def clean_table(tab):
    # longitude hors champs 
    tab = tab[tab['longitude'] < 50]
#    print(tab.longitude.nunique())
    # debug in timestamps   
    tab['delta'] = tab['timestamp'] - tab['timestamp'].shift(1)
    # deplacement
    tab['diff_lat'] = tab['latitude'] - tab['latitude'].shift(1)
    tab['diff_lon'] = tab['longitude'] - tab['longitude'].shift(1)
    immobile = (tab['diff_lat'] == 0) & (tab['diff_lon'] == 0)
    tab = tab[~immobile]
    
#    print('point sans mouvement : ', sum(immobile))
#    print('nombre de déplacement : ', sum(~immobile))
    try:
        check_table(tab)
    except:
        cond_time = tab['delta'] <= 0
        import pdb; pdb.set_trace()

    return tab


def transform_to_js(tab, name_js, limit_len_inf = 1, limit_len_sup = None):
    if len(tab) >= limit_len_inf:
        with open("data\\" + name_js + '.js', mode='w') as f:
            f.write('var ' + name_js + ' = { \n' + init_js)   
            timestamps = []
            if limit_len_sup is not None:
                if len(tab) > limit_len_sup:
                    tab = tab.iloc[:limit_len_sup]
            for i, row in tab.iterrows():
                line = '\t\t[\n \t\t  ' + str(row['longitude']) + ',\n \t\t  ' + \
                    str(row['latitude']) + '\n \t\t], \n'
                f.write(line)
                timestamps += [str(int(row['timestamp']))]
            assert len(timestamps) == i + 1
            f.write(intermediate_js + '\t\t' + ',\n\t\t'.join(timestamps) + ',\n\t\t],')
            f.write('\n\t}\n}')


for id_ in tab.id.unique():
    tab_id = tab[tab.id == id_]
    tab_id.sort(columns = 'timestamp', inplace=True)
    tab_id.reset_index(inplace=True)
    
    # debug
    if id_ in [600104101]:
        delta = tab_id['timestamp'] - tab_id['timestamp'].shift(1)
        tab_id = tab_id[delta == 0] #TODO: c'est celui d'avant qu'il faudrait retirer
    
    print(str(id_))
    tab_id = clean_table(tab_id)
    
    tab_id.reset_index(inplace=True)

    print(str(id_))
    transform_to_js(tab_id, 'id_' + str(id_), limit_len_inf = 2, limit_len_sup = 3)


#test = tab[tab.id == id_]
#test = test[['latitude','longitude','timestamp']]
#test = test.sort('timestamp')