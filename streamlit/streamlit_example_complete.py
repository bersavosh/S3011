import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import seaborn as sns

# Markdown
#st.write("# A simple Dashboard")
# or
"# A simple Streamlit Dashboard"
"In this example we make a simple streamlit dashboard."
"The text is Markdown, with features like latex ($\int x^2 dx$), etc."

"## Data"
"The data we will use is meteorology data for some cities in Europe. \
Let's First tabulate the data."

data = pd.read_csv('../data/weather_data.csv')

"### Dynamic display of a table"
"You can sort and tweak sizes."
#st.write(data)
# or
data

"### Static display of a table"
"Our dataset is too long for a static display, so we only display the first few rows:"
st.table(data.head())

'## Visualization using Streamlit native functions'

data['DATE'] = pd.to_datetime(data['DATE'],format='%Y%m%d')

'Percipitation'
st.bar_chart(data,x='DATE',y=['BASEL_precipitation','BUDAPEST_precipitation'])


'Temparture'
st.line_chart(data,x='DATE',y=['BASEL_temp_mean','BUDAPEST_temp_mean'])

basel_2000_avgT = data['BASEL_temp_mean'][(data['DATE'] > '2000-04-01') & (data['DATE'] < '2000-07-01')].mean()
basel_2009_avgT = data['BASEL_temp_mean'][(data['DATE'] > '2009-04-01') & (data['DATE'] < '2009-07-01')].mean()

budapest_2000_avgT = data['BUDAPEST_temp_mean'][(data['DATE'] > '2000-04-01') & (data['DATE'] < '2000-07-01')].mean()
budapest_2009_avgT = data['BUDAPEST_temp_mean'][(data['DATE'] > '2009-04-01') & (data['DATE'] < '2009-07-01')].mean()

col1, col2 = st.columns(2)
with col1:
    basel_T_metric = st.metric(label='Summer Temperature in Basel (C)',
                               value=round(basel_2009_avgT,2), 
                               delta=round(basel_2009_avgT-basel_2000_avgT,2),
                               delta_color='inverse')

with col2:
    st.metric(label='Summer Temperature in Budapest (C)',
                              value=round(budapest_2009_avgT,2), 
                              delta=round(budapest_2009_avgT-budapest_2000_avgT,2),
                              delta_color='inverse',
                              help='Temperature Average calculated between March and Septemter of 2009, compared to the same period in 2000')


"## Adding a matplotlib figure"
"we can add a static matplotlib plot"

months = ['January','February','March',
          'April','May','June',
          'July','August','September',
          'October','November','December']
theme_color = [0.15,0.17,0.22,0.1]

fig = plt.figure(facecolor=theme_color)
ax = fig.add_subplot(1,1,1, projection='polar',facecolor=theme_color)
ax.plot(np.deg2rad(data['DATE'].dt.day_of_year*360/365),data['BASEL_temp_mean'],alpha=0.9,lw=0.5,color='deepskyblue',label='Basel')
ax.plot(np.deg2rad(data['DATE'].dt.day_of_year*360/365),data['BUDAPEST_temp_mean'],alpha=0.9,lw=0.5,color='b',label='Budapest')
ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
ax.set_xticklabels(months,color='0.5')
ax.yaxis.set_tick_params(labelcolor='0.5')
ax.spines[:].set_color('0.5')
ax.legend(facecolor=theme_color,labelcolor='w',bbox_to_anchor=[1.2,1.1])

st.write(fig)

"## Dynamic visualizations using Altair"

c = alt.Chart(data).mark_circle().encode(
        x='BASEL_sunshine',
        y='BASEL_cloud_cover',
        color='BASEL_temp_mean',
        tooltip=['BASEL_humidity','DATE']).interactive()

st.altair_chart(c,use_container_width=True)

"## Using sliders/widgets"

"### Method 1: through streamlit slider"
"Comparatively slow, but works seamlessly across elements"

sldr_month = st.slider('Month of year',min_value=1,max_value=12,step=1)
month_data = data[data['MONTH']==sldr_month]
c2 = alt.Chart(month_data).mark_bar().encode(
         alt.X('BASEL_precipitation',bin=True),
         y='count()')

c3 = alt.Chart(month_data).mark_bar().encode(
         alt.X('BUDAPEST_precipitation',bin=True),
         y='count()')

st.altair_chart(alt.concat(c2,c3))

"### Method 2: through altair"
"Much faster but more complex to use between non-altair elements"

alt_slider = alt.binding_range(min=1, max=12, step=1)
selector = alt.selection_single(name='month', fields=['MONTH'],
                                bind=alt_slider)

c4 = alt.Chart(data).mark_bar().encode(
         alt.X('BUDAPEST_precipitation',bin=True),
         y='count()').add_params(selector).transform_filter(selector)

st.write(c4)

"""
st.write('## A GraphViz graph')
st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')
"""