
# coding: utf-8

# In[321]:

import pandas as pd


# In[322]:

df1_1 = pd.read_excel('data/indonesia/1-indonesia-eiti-projects.xlsx', sheetname='EITI project level data sample')
df1_1['source'] = 'indonesia-eiti-projects'
df1_2 = pd.read_excel('data/indonesia/1-indonesia-eiti-projects.xlsx', sheetname='Mining license sample')
df1_2['source'] = 'indonesia-mining-licenses'
df1_2['country'] = 'Indonesia' # Check that this is correct (ie. that this sheet is all Indonesia)


# In[323]:

df2 = pd.read_csv('data/minfac.csv', encoding='latin-1')
df2['source'] = 'usgs'
df3 = pd.read_csv('data/indonesia/3-openoil-concessions-indonesia.csv')
df3['source'] = 'indonesia-openoil-concessions'
df3['country'] = 'Indonesia'
df4 = pd.read_csv('data/indonesia/4-openoil-contracts-indonesia.csv')
df4['source'] = 'indonesia-openoil-contracts'
df4['country'] = 'Indonesia'


# In[324]:

for df in [df1_1, df1_2, df3, df4]:
    df.columns = map(str.lower, df.columns)
    df.columns = [str.lower(x).replace(' / ', '_').replace(' ', '_').replace('?', '').replace('(us$)', 'usd') for x in df.columns]
#df.rename(columns={
#        'Country': 'country',
#    })
df1_1 = df1_1.rename(columns={
        'commodity_type': 'commodity',
    })
df1_2 = df1_2.rename(columns={
        'komoditas / commodity?': 'commodity',
        'tahun': 'year',
        'nama_perusahaan / company name': 'company_name'
    })
df2 = df2.rename(columns={
        'op_comp': 'company_name',
        'capacity': 'production_volume',  # Not 100% sure these are the same, needs checking
        'units': 'production_unit',  # Not 100% sure these are the same, needs checking
    })
df3 = df3.rename(columns={
        'concessioncontractor': 'company_name',
    })
df4 = df4.rename(columns={
        'contractor': 'company_name',
    })


# In[325]:

combined_df = pd.concat([df1_1, df1_2, df2, df3, df4])


# In[326]:

fields = combined_df.groupby('source').count().transpose()
fields


# In[327]:

sources_per_field = fields.apply(lambda x: x>0).sum(axis=1)
sources_per_field.sort(ascending=False)
sources_per_field


# In[328]:

df_idn = combined_df[combined_df['country'] == 'Indonesia']
fields = combined_df.groupby('source').count().transpose()
fields


# In[365]:

company_names_by_source = df_idn.groupby('company_name')['source'].nunique()
company_names_by_source.sort(ascending=False)
company_names_gt1_source = company_names_by_source[company_names_by_source > 1]
company_names_gt1_source


# In[366]:

#for name, group in df_idn.groupby('company_name')['source']:
#    if group.nunique() > 1:
#        print(name)
#        print(group.value_counts())


# In[380]:

sources = df_idn.source.unique()
series = [ pd.Series(df_idn[df_idn['source'] == source].company_name.unique()) for source in sources ]
df = pd.concat(series, axis=1)
df.columns = df_idn.source.unique()
df.count()


# In[383]:

df

