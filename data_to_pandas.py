import pandas as pd
from collections import OrderedDict

data_frames = OrderedDict()

data_frames['indonesia-eiti-projects'] = pd.read_excel('data/indonesia/1-indonesia-eiti-projects.xlsx', sheetname='EITI project level data sample')
data_frames['indonesia-mining-licenses'] = pd.read_excel('data/indonesia/1-indonesia-eiti-projects.xlsx', sheetname='Mining license sample')
data_frames['indonesia-mining-licenses']['country'] = 'Indonesia' # Check that this is correct (ie. that this sheet is all Indonesia)

data_frames['usgs'] = pd.read_csv('data/minfac.csv', encoding='latin-1')

data_frames['indonesia-openoil-concessions'] = pd.read_csv('data/indonesia/3-openoil-concessions-indonesia.csv')
data_frames['indonesia-openoil-concessions']['country'] = 'Indonesia'

data_frames['indonesia-openoil-contracts'] = pd.read_csv('data/indonesia/4-openoil-contracts-indonesia.csv')
data_frames['indonesia-openoil-contracts']['country'] = 'Indonesia'

MAPPINGS = OrderedDict()
MAPPINGS['indonesia-eiti-projects'] = {
        'commodity_type': 'commodity',
    }
MAPPINGS['indonesia-mining-licenses'] = {
        'komoditas / commodity?': 'commodity',
        'tahun': 'year',
        'nama_perusahaan / company name': 'company_name'
    }
MAPPINGS['usgs'] = {
        'op_comp': 'company_name',
        'capacity': 'production_volume',  # Not 100% sure these are the same, needs checking
        'units': 'production_unit',  # Not 100% sure these are the same, needs checking
    }
MAPPINGS['indonesia-openoil-concessions'] = {
        'concessioncontractor': 'company_name',
    }
MAPPINGS['indonesia-openoil-contracts'] = {
        'contractor': 'company_name',
    }

for key, df in data_frames.items():
    df['source'] = key

    df.columns = map(str.lower, df.columns)
    df.columns = [str.lower(x).replace(' / ', '_').replace(' ', '_').replace('?', '').replace('(us$)', 'usd') for x in df.columns]

    data_frames[key] = df.rename(columns=MAPPINGS[key])
