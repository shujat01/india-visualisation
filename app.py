import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.express as px 
import base64
from io import BytesIO
import plotly.io as pio
import plotly.graph_objects as go


# Configure the app
st.set_page_config(layout='wide', page_title="India Visualization App", page_icon="🇮🇳")

# Custom CSS
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.stSelectbox > div > div > div {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# Load and cache the data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('india.csv')
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please check if 'india.csv' exists in the current directory.")
        return None

df = load_data()

if df is not None:
    # Define pages    
    def india_scatter_map():
        st.markdown('<p class="big-font">India Visualization App - Scatter Map</p>', unsafe_allow_html=True)
        st.write("BY: Shujjad")

        list_of_states = ['Overall India'] + sorted(df['State'].unique())
        selected_state = st.sidebar.selectbox('Select State', list_of_states)
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        primary = st.sidebar.selectbox('Select Primary Parameter', sorted(numeric_columns))
        secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(numeric_columns))
        
        plot = st.sidebar.button('Plot Graph')

        if plot:
            st.info('Size represents primary parameter')
            st.info('Color represents secondary parameter')

            try:
                if selected_state == 'Overall India':
                    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=4, size_max=35,
                                            mapbox_style="carto-positron", width=1200, height=700, hover_name='District')
                else:
                    state_df = df[df['State'] == selected_state]
                    fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=primary, color=secondary, zoom=6, size_max=35,
                                            mapbox_style="carto-positron", width=1200, height=700, hover_name='District')
                
                st.plotly_chart(fig)
                
                # Add download button
                buf = BytesIO()
                fig.write_image(buf, format="png")
                btn = st.download_button(
                    label="Download graph",
                    data=buf.getvalue(),
                    file_name="scatter_map.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"An error occurred while plotting: {str(e)}")

    def india_choropleth_map():
        st.markdown('<p class="big-font">India Visualization App - Choropleth Map</p>', unsafe_allow_html=True)
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        selected_parameter = st.sidebar.selectbox('Select Parameter', sorted(numeric_columns))
        
        plot = st.sidebar.button('Plot Map')

        if plot:
            try:
                state_data = df.groupby('State')[selected_parameter].mean().reset_index()
                
                fig = px.choropleth(
                    state_data,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color=selected_parameter,
                    color_continuous_scale='Viridis',
                    title=f'{selected_parameter} by State',
                    width=1200,
                    height=700
                )

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
                
                # Modified download button
                buf = BytesIO()
                fig.write_image(buf, format="png")
                btn = st.download_button(
                    label="Download map",
                    data=buf.getvalue(),
                    file_name="choropleth_map.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"An error occurred while plotting: {str(e)}")

    def trend_analysis():
        st.markdown('<p class="big-font">India Visualization App - Trend Analysis</p>', unsafe_allow_html=True)
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        x_axis = st.sidebar.selectbox('Select X-axis Parameter', sorted(numeric_columns))
        y_axis = st.sidebar.selectbox('Select Y-axis Parameter', sorted(numeric_columns))
        
        plot = st.sidebar.button('Plot Trend')

        if plot:
            try:
                # Create scatter plot
                fig = px.scatter(df, x=x_axis, y=y_axis, color='State', 
                                 hover_name='District',
                                 title=f'Trend Analysis: {y_axis} vs {x_axis}',
                                 width=1200, height=700)
                
                # Calculate and add trendline
                z = np.polyfit(df[x_axis], df[y_axis], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(x=df[x_axis], y=p(df[x_axis]),
                                         mode='lines', name='Trendline',
                                         line=dict(color='red', dash='dash')))
                
                st.plotly_chart(fig)
                
                # Modified download button
                buf = BytesIO()
                fig.write_image(buf, format="png")
                btn = st.download_button(
                    label="Download graph",
                    data=buf.getvalue(),
                    file_name="trend_analysis.png",
                    mime="image/png"
                )

                # Calculate and display correlation
                correlation = df[x_axis].corr(df[y_axis])
                st.write(f"Correlation between {x_axis} and {y_axis}: {correlation:.2f}")

            except Exception as e:
                st.error(f"An error occurred while plotting: {str(e)}")

    def india_scatter_plot():
        st.markdown('<p class="big-font">India Visualization App - Scatter Plot</p>', unsafe_allow_html=True)
        
        list_of_states = ['Overall India'] + sorted(df['State'].unique())
        selected_state = st.sidebar.selectbox('Select State', list_of_states)
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        x_axis = st.sidebar.selectbox('Select X-axis Parameter', sorted(numeric_columns))
        y_axis = st.sidebar.selectbox('Select Y-axis Parameter', sorted(numeric_columns))
        
        plot = st.sidebar.button('Plot Graph')

        if plot:
            try:
                if selected_state == 'Overall India':
                    fig = px.scatter(df, x=x_axis, y=y_axis, width=1200, height=700, color="State", hover_name='State')
                else:
                    state_df = df[df['State'] == selected_state]
                    fig = px.scatter(state_df, x=x_axis, y=y_axis, width=1200, height=700, color='District', hover_name='District')
                
                st.plotly_chart(fig)
                
                # Add download button
                buf = BytesIO()
                fig.write_image(buf, format="png")
                btn = st.download_button(
                    label="Download graph",
                    data=buf.getvalue(),
                    file_name="scatter_plot.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"An error occurred while plotting: {str(e)}")

    def data_summary():
        st.markdown('<p class="big-font">Data Summary</p>', unsafe_allow_html=True)
        
        st.write(df.describe())
        
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        st.subheader("Missing Values")
        missing_data = df.isnull().sum()
        st.write(missing_data[missing_data > 0])
        
        st.subheader("Correlation Matrix")
        corr_matrix = df.select_dtypes(include=[np.number]).corr()
        fig = px.imshow(corr_matrix, color_continuous_scale='RdBu_r', aspect="auto")
        st.plotly_chart(fig)

    # Sidebar for navigation
    pages = {
        "Scatter Map": india_scatter_map,
        "Choropleth Map": india_choropleth_map,
        "Trend Analysis": trend_analysis,
        "Scatter Plot": india_scatter_plot,
        "Data Summary": data_summary
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Select a Page", options=list(pages.keys()))
    pages[selected_page]()

else:
    st.error("Unable to load data. Please check your data file and try again.")
