# Import warnings library
import warnings 
# Set action = "ignore" to ignore warnings
warnings.filterwarnings(action= 'ignore')

import numpy as np
import seaborn as sns
from numpy import linalg as la
import matplotlib.pyplot as plt

import folium
from folium.features import DivIcon
from folium import plugins

import statsmodels.formula.api as smf
import statsmodels.api as sm

import pandas as pd

def plot_borders(gdf, name):
    fig = plt.figure(figsize=(12,15))
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    gdf.plot(ax=ax, color='white', edgecolor='black')
    plt.xlim([8.0, 16])
    plt.ylim([54.4, 58])
    plt.show()
    plt.savefig(name);

    
def map_plot(df, gdf, data, size):
    start_loc=(df.iloc[0].long, df.iloc[0].lat)
    df = df.sample(size)
    m = folium.Map(location=start_loc, zoom_start=7, tiles='cartodbpositron')
    folium.GeoJson(data.json()).add_to(m)


    for i in range(df.shape[0]):
        row= df.iloc[i]
        poi= (row.long, row.lat)
        poi_name = row.Adresse
        folium.CircleMarker(location=poi, color='red', radius=1, fill='red').add_to(m)
        # Display POI Name
        folium.map.Marker(location=poi, icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 7pt; color: red">{}</div>'.format(poi_name)
        )).add_to(m)
        mids = []
        for i in row.distance_to_mun[2]:
            a = (i.coords.xy[1][0],i.coords.xy[0][0])
            b = (i.coords.xy[1][1],i.coords.xy[0][1])
            mids.append(((a[0]+b[0])/2, (a[1]+b[1])/2))
            folium.PolyLine(locations=[a,b], color='red').add_to(m)

        for it, dist in enumerate(row.distance_to_mun[1]):
            folium.map.Marker(location=mids[it], icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html='<div style="font-size: 6pt; color: red">Distance: {} Meters</div>'.format(round(dist))
            )).add_to(m)
    m.save('Dist_map.html')
    
def map_plot_ex(df, gdf, data, size):
    '''
    Show copenhagen vs frederiksberg
    '''
    #subset to only contain Copenhagen and frederiksberg
    
    ex = df
    ex1 = ex[ex.Kommune == 'København']
    ex2 = ex[ex.Kommune == 'Frederiksberg']
    df = pd.concat([ex1,ex2])
    

    start_loc=(df.iloc[0].long, df.iloc[0].lat)
    df = df.sample(size)
    m = folium.Map(location=start_loc, zoom_start=7, tiles='cartodbpositron')
    folium.GeoJson(gdf.geometry.boundary.to_json()).add_to(m)


    for i in range(df.shape[0]):
        row= df.iloc[i]
        poi= (row.long, row.lat)
        #poi_name = row.Adresse
        folium.CircleMarker(location=poi, color='red', radius=1, fill='red').add_to(m)
        # Display POI Name
        #folium.map.Marker(location=poi, icon=DivIcon(
         #   icon_size=(150, 36),
         #   icon_anchor=(0, 0),
         #   html='<div style="font-size: 7pt; color: red">{}</div>'.format(poi_name)
        #)).add_to(m)
        mids = []
        
        # maybe index row.distance_to_mun[2][0] and make round(dist) to negative in København
        c = 0
        for i in row.distance_to_mun[2]:
            if c ==1:
                break
            a = (i.coords.xy[1][0],i.coords.xy[0][0])
            b = (i.coords.xy[1][1],i.coords.xy[0][1])
            mids.append(((a[0]+b[0])/2, (a[1]+b[1])/2))
            folium.PolyLine(locations=[a,b], color='red').add_to(m)
            c+=1
        for it, dist in enumerate(row.distance_to_mun[1]):
            if it ==1:
                break
            if row.Kommune == 'København':
                dist = -dist
            folium.map.Marker(location=mids[it], icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html='<div style="font-size: 6pt; color: red">Distance: {} Meters</div>'.format(round(dist))
            )).add_to(m)
    m.save('Dist_map_ex.html')

    
    
    
def plot(data, x, y, hue):
    sns.set_theme(style="whitegrid")
    cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
    g = sns.relplot(
        data=data,
        x=x, y=y,
        hue=hue,
        palette=cmap, sizes=(10, 200),
    )
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, "minor", linewidth=.25)
    g.despine(left=True, bottom=True);
    



def replace(string):
        if string == 'coef':
            return string.replace(" ", "_")
        elif string == 'P>|t|':
            return 'Pt'
        elif string == "[0.025":
            return "low"
        elif string == '0.975]':
            return "high"
        else: pass
def kernel(R, c, h):
    indicator = (np.abs(R-c) <= h).astype(float)
    return indicator * (1 - np.abs(R-c)/h)

def RDD(df, list_of_neighbors, reg, kernel_w = False):

    min_y = df.Year.min()
    max_y = df.Year.max()
    var = ['log_price', 'Distance_sign', 'Border_dummy', 'Grundskylds_promille']
    tax_diff = []
    rows= []
    row_index = []
    n = []
    for i in range(len(list_of_neighbors)):
        df_ = df[df.Neighbors_set == str(list_of_neighbors[i])]
        n_set = list_of_neighbors[i]
        for j in range(max_y - min_y):
            y = min_y + j
            f = df_[df_.Year == y]
            f = f.sort_values(by=['Distance_sign'])
            if len(f.Kommune.value_counts()) == 2:
          
                if f.Kommune.value_counts()[0] > 100:
                    if f.Kommune.value_counts()[1] > 100:
                    
                        tax_diff.append(abs(f.Tax_diff.iloc[0]))
                        n.append(f.shape[0])
                        

                        if kernel:
                            k = kernel(f["Distance_sign"], c=0, h=5000)
                            model = smf.wls(reg, f,weights=k).fit(cov_type='HC1')
                            model_as_html = model.summary().tables[1].as_html()
                        else:
                            model = smf.wls(reg, f).fit(cov_type='HC1')
                            model_as_html = model.summary().tables[1].as_html()
                        tab = pd.read_html(model_as_html, header=0, index_col=0)[0]
                        
                        row = tab.iloc[2]
                        row_index.append(f'{n_set[0]}_{n_set[1]}_{y}')
                        rows.append(row)
                    else: pass
                else:pass
                
            else: pass
    data =pd.DataFrame(rows)
    data['Tax_diffs'] = tax_diff
    data['n'] =n
    data.index = row_index
    return data



def reg(df):

    #df['Tax_diffs2'] = df['Tax_diffs'] **2
    
    results = smf.ols('coef ~ Tax_diffs ', data=df).fit()
    res = results.summary().tables[1].as_html()
    tab = pd.read_html(res, header=0, index_col=0)[0]
    return results, tab

def table_col(df):
    index_label = []
    for i in df.index:
        index_label.append(i)
        index_label.append('')

    col = []

    for i in range(df.shape[0]):
        row = df.iloc[i]
        if row['P>|t|'] <0.01:
            coef_ = f'{row.coef}'+'^{***}'
        elif row['P>|t|'] <0.05:
            coef_ = f'{row.coef}'+'^{**}'
        elif row['P>|t|'] <0.1:
            coef_ = f'{row.coef}'+'^{*}'
        else: coef_ = f'{row.coef}'
        col.append(coef_)
        stderr =row['std err']
        col.append(f'({stderr})')


    res_df = pd.DataFrame(col,index=index_label )
    return res_df

def table_col_RD(df):
    index_label = []
    for i in df.index:
        index_label.append(i)
        index_label.append('')

    col = []

    for i in range(df.shape[0]):
        row = df.iloc[i]
        if row['P>|z|'] <0.01:
            coef_ = f'${row.coef}'+'^{***}$'
        elif row['P>|z|'] <0.05:
            coef_ = f'${row.coef}'+'^{**}$'
        elif row['P>|z|'] <0.1:
            coef_ = f'${row.coef}'+'^{*}$'
        else: coef_ = f'{row.coef}'
        col.append(coef_)
        stderr =row['std err']
        col.append(f'({stderr})')


    res_df = pd.DataFrame(col,index=index_label )
    return res_df