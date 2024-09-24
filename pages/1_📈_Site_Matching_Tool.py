import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely import centroid
from PIL import Image

@st.cache_resource
def addlogo():
    st.image(Image.open('data/national-trust-logo.png'), width=500)

addlogo()
st.title('Site Matching Tool')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/' 'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


def load_data():
    gpd_data = np.load('data/ntrust_data.npy', allow_pickle=True)
    data = pd.DataFrame(data=gpd_data, columns=["Name", "Region", "Mean temperature (current)", "Mean temperature (future)", "Min temperature (current)", "Min temperature (future)", "Max temperature (current)", "Max temperature (future)", "Sunshine exposure (current)", "Growing degree days (current)", "Growing degree days (future)", "Heating demand (current)", "Heating demand (future)", "Cooling demand (current)", "Cooling demand (future)", "10mm rain likelihood (current)", "10mm rain likelihood (future)", "Mansion", "Area (ha)", "latitude", "longitude"])
    labels = []
    tab_regions = list(data['Region'])
    tab_names = list(data['Name'])
    urls = []
    for i in range(len(tab_regions)):
        s = '(%s) %s' % (tab_regions[i], tab_names[i])
        labels.append('(%s) %s' % (tab_regions[i], tab_names[i]))
        urls.append('https://www.nationaltrust.org.uk/site-search#gsc.tab=0&gsc.q=%s&gsc.sort=' % tab_names[i])
    data['Property name'] = labels
    data['Website URL'] = urls
    labels = sorted(labels)
    
    glob = {}
    glob[('min', "Mean temperature (current)")] = min(data["Mean temperature (current)"])
    glob[('min', "Mean temperature (future)")] = min(data["Mean temperature (future)"])
    glob[('min', "Min temperature (current)")] = min(data["Min temperature (current)"])
    glob[('min', "Min temperature (future)")] = min(data["Min temperature (future)"])
    glob[('min', "Max temperature (current)")] = min(data["Max temperature (current)"])
    glob[('min', "Max temperature (future)")] = min(data["Max temperature (future)"])
    glob[('min', "Sunshine exposure (current)")] = min(data["Sunshine exposure (current)"])
    glob[('min', "Growing degree days (current)")] = min(data["Growing degree days (current)"])
    glob[('min', "Growing degree days (future)")] = min(data["Growing degree days (future)"])
    glob[('min', "Heating demand (current)")] = min(data["Heating demand (current)"]) 
    glob[('min', "Heating demand (future)")] = min(data["Heating demand (future)"])
    glob[('min', "Cooling demand (current)")] = min(data["Cooling demand (current)"]) 
    glob[('min', "Cooling demand (future)")] = min(data["Cooling demand (future)"])
    glob[('min', "10mm rain likelihood (current)")] = min(data["10mm rain likelihood (current)"]) 
    glob[('min', "10mm rain likelihood (future)")] = min(data["10mm rain likelihood (future)"])
    glob[('min', "Area (ha)")] = min(data["Area (ha)"])
    glob[('max', "Mean temperature (current)")] = max(data["Mean temperature (current)"])
    glob[('max', "Mean temperature (future)")] = max(data["Mean temperature (future)"])
    glob[('max', "Min temperature (current)")] = max(data["Min temperature (current)"])
    glob[('max', "Min temperature (future)")] = max(data["Min temperature (future)"])
    glob[('max', "Max temperature (current)")] = max(data["Max temperature (current)"])
    glob[('max', "Max temperature (future)")] = max(data["Max temperature (future)"])
    glob[('max', "Sunshine exposure (current)")] = max(data["Sunshine exposure (current)"])
    glob[('max', "Growing degree days (current)")] = max(data["Growing degree days (current)"])
    glob[('max', "Growing degree days (future)")] = max(data["Growing degree days (future)"])
    glob[('max', "Heating demand (current)")] = max(data["Heating demand (current)"]) 
    glob[('max', "Heating demand (future)")] = max(data["Heating demand (future)"])
    glob[('max', "Cooling demand (current)")] = max(data["Cooling demand (current)"]) 
    glob[('max', "Cooling demand (future)")] = max(data["Cooling demand (future)"])
    glob[('max', "10mm rain likelihood (current)")] = max(data["10mm rain likelihood (current)"]) 
    glob[('max', "10mm rain likelihood (future)")] = max(data["10mm rain likelihood (future)"])
    glob[('max', "Area (ha)")] = max(data["Area (ha)"])
    
    return data, labels, glob

def compute_distances(data, disthash, name_mapping, label):
    distances = []
    for name, region in zip(data['Name'], data['Region']):
        s = "(%s) %s" % (region, name)
        distances.append(disthash[name_mapping[label], name_mapping[s]])
    distances = np.array(distances)
    distances = np.max(distances) - distances
    distances = distances / np.max(distances)
    dist_list = sorted(list(distances))
    return distances, dist_list

def set_filtereddata_n(data, dist_list, n_thr):
    similarity_thr = dist_list[len(dist_list)-(n_thr+1)]
    tmp_filtered_data = data.loc[(data["Similarity"]>=similarity_thr)]
    return tmp_filtered_data
    

def get_filters_n(data, dist_list, n_thr):
    similarity_thr = dist_list[len(dist_list)-n_thr]
    tmp_filtered_data = data.loc[(data["Similarity"]>=similarity_thr)]
    H = {}
    
    for key in ["Mean temperature (current)", "Mean temperature (future)", "Min temperature (current)", "Min temperature (future)", "Max temperature (current)", "Max temperature (future)", "Sunshine exposure (current)", "Growing degree days (current)", "Growing degree days (future)", "Heating demand (current)", "Heating demand (future)", "Cooling demand (current)", "Cooling demand (future)", "10mm rain likelihood (current)", "10mm rain likelihood (future)", "Area (ha)"]:
        H[key] = (min(tmp_filtered_data[key]), max(tmp_filtered_data[key]))
    
    return H

def delete_session_state():
    for key in ["Mean temperature (current)", "Mean temperature (future)", "Min temperature (current)", "Min temperature (future)", "Max temperature (current)", "Max temperature (future)", "Sunshine exposure (current)", "Growing degree days (current)", "Growing degree days (future)", "Heating demand (current)", "Heating demand (future)", "Cooling demand (current)", "Cooling demand (future)", "10mm rain likelihood (current)", "10mm rain likelihood (future)", "Area (ha)"]:
        if key in st.session_state:
            del st.session_state[key]



(data, labels, glob) = load_data()

st.header(':european_castle:    Site selection')
option = st.selectbox("Select your site:", labels, on_change=delete_session_state)



st.header(':toolbox:    Matching')
n_thr = st.slider('Number of sites to match with', 1, len(labels), 10, on_change=delete_session_state)

#fake_options = st.multiselect('Match by', ["Current Climate", "Future Climate", "Building Type", "Garden Type", "Site Usage"], ["Current Climate", "Future Climate", "Building Type", "Garden Type", "Site Usage"])
st.write('Match by:')
bout = ""
if st.checkbox(label="Current climate data", value=True):
    bout += "c"
if st.checkbox(label="Future climate data", value=True):
    bout += "f"
if st.checkbox(label="Property data", value=True):
    bout += "p"

if len(bout) == 0:
    bout = "cfp"
    
disthash = np.load('data/distmap_%s.npy' % bout)
name_mapping = np.load('data/name_mapping.npy', allow_pickle=True).any()
distances, dist_list = compute_distances(data, disthash, name_mapping, option)
data['Similarity'] = distances
tmp_filtered_data = set_filtereddata_n(data, dist_list, n_thr)

st.header(':bar_chart:    Matched sites')
st.map(tmp_filtered_data)


matched_sites = tmp_filtered_data[['Property name', 'Similarity', 'Website URL', 'Mean temperature (current)', 'Mean temperature (future)', 'Min temperature (current)', 'Min temperature (future)', 'Max temperature (current)', 'Max temperature (future)', 'Sunshine exposure (current)', 'Mansion', 'Area (ha)', 'latitude', 'longitude']].sort_values(by="Similarity", ascending=False)
matched_sites.index = [''] + list(range(1, len(matched_sites.index)))
#matched_sites.style.applymap(lambda _: "background-color: CornflowerBlue;", subset=([1], slice(None)))
st.subheader('Details')
st.dataframe(matched_sites.iloc[1:], column_config={
    "Website URL": st.column_config.LinkColumn(display_text="Link")
})
