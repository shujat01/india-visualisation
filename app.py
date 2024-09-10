import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.express as px 

st.set_page_config(layout='wide')

# Load the data
df = pd.read_csv('india.csv')

# Define pages    
def india_scatter_map():
    st.title("India Visualization App")
    st.write("BY :-Shujjad Ali")
    st.sidebar.title('Scatter Map')

    list_of_states = list(df['State'].unique())
    list_of_states.insert(0, 'Overall India')

    selected_state = st.sidebar.selectbox('Select State', list_of_states)
    primary = st.sidebar.selectbox('Select Primary Parameter', sorted(list(df.columns[5:6]) + list(df.columns[13:16]) + list(df.columns[18:])))
    secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(list(df.columns[5:6]) + list(df.columns[13:16]) + list(df.columns[18:])))
    plot = st.sidebar.button('Plot Graph')

    if plot:
        st.text('Size represents primary parameter')
        st.text('Color represents secondary parameter')

        if selected_state == 'Overall India':
            fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=4, size_max=35,
                                    mapbox_style="carto-positron", width=1200, height=700, hover_name='District')
        else:
            state_df = df[df['State'] == selected_state]
            fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=4, size_max=35,
                                    mapbox_style="carto-positron", width=1200, height=700, hover_name='District')
        
        st.plotly_chart(fig)

def india_bar_chart():
    st.title("India Visualization App")
    
    st.sidebar.title('Bar Chart')
    list_of_states = list(df['State'].unique())
    list_of_states.insert(0, 'Overall India')

    selected_state = st.sidebar.selectbox('Select State', list_of_states)
    
    x_axis = st.sidebar.selectbox('Select X-axis Parameter', sorted(list(df.columns[5:6]) + list(df.columns[13:16]) + list(df.columns[18:])))
    y_axis = st.sidebar.selectbox('Select Y-axis Parameter', sorted(list(df.columns[5:6]) + list(df.columns[13:16]) + list(df.columns[18:])))
    plot = st.sidebar.button('Plot Graph')

    if plot:

        if selected_state == 'Overall India':
            fig = px.bar(df,x=x_axis,y=y_axis, width=1200, height=700,hover_name='State')
        else:
            state_df = df[df['State'] == selected_state]
            fig = px.bar(state_df,x=x_axis,y=y_axis,width=1200, height=700, hover_name='District')
        
        st.plotly_chart(fig)

def india_scatter_plot():
    st.title("India Visualization App")
    
    st.sidebar.title('Scatter Plot')
    list_of_states = list(df['State'].unique())
    list_of_states.insert(0, 'Overall India')

    selected_state = st.sidebar.selectbox('Select State', list_of_states)
    
    x_axis = st.sidebar.selectbox('Select X-axis Parameter', sorted(list(df.columns[5:6]) + list(df.columns[13:16]) + list(df.columns[18:])))
    y_axis = st.sidebar.selectbox('Select Y-axis Parameter', sorted(list(df.columns[5:6]) + list(df.columns[13:16]) + list(df.columns[18:])))
    plot = st.sidebar.button('Plot Graph')

    if plot:

        if selected_state == 'Overall India':
            fig = px.scatter(df,x=x_axis,y=y_axis, width=1200, height=700, color="State",hover_name='State')
        else:
            state_df = df[df['State'] == selected_state]
            fig = px.scatter(state_df,x=x_axis,y=y_axis,width=1200, height=700, hover_name='District')
        
        st.plotly_chart(fig)


# Sidebar for navigation
pages = {
    "Scatter Map": india_scatter_map,
    "Bar Chart": india_bar_chart,
    "Scatter Plot":india_scatter_plot
    # Add other pages here
}

selected_page = st.sidebar.selectbox("Select a Graph", options=list(pages.keys()))
pages[selected_page]()
