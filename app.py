import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.express as px 
import base64
from io import BytesIO
import plotly.io as pio


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

    def india_bar_chart():
        st.markdown('<p class="big-font">India Visualization App - Bar Chart</p>', unsafe_allow_html=True)
        
        list_of_states = ['Overall India'] + sorted(df['State'].unique())
        selected_state = st.sidebar.selectbox('Select State', list_of_states)
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        x_axis = st.sidebar.selectbox('Select X-axis Parameter', sorted(numeric_columns))
        y_axis = st.sidebar.selectbox('Select Y-axis Parameter', sorted(numeric_columns))
        
        aggregation = st.sidebar.selectbox('Select Aggregation', ['sum', 'mean', 'median', 'min', 'max'])
        top_n = st.sidebar.number_input('Top N entries', min_value=1, max_value=50, value=10)
        
        plot = st.sidebar.button('Plot Graph')

        if plot:
            try:
                if selected_state == 'Overall India':
                    grouped_df = df.groupby('State').agg({x_axis: aggregation, y_axis: aggregation}).reset_index()
                    grouped_df = grouped_df.sort_values(y_axis, ascending=False).head(top_n)
                    fig = px.bar(grouped_df, x='State', y=y_axis, color=x_axis, 
                                 labels={y_axis: f'{y_axis} ({aggregation})', x_axis: f'{x_axis} ({aggregation})'},
                                 title=f'Top {top_n} States by {y_axis} ({aggregation})',
                                 width=1200, height=700)
                else:
                    state_df = df[df['State'] == selected_state]
                    grouped_df = state_df.groupby('District').agg({x_axis: aggregation, y_axis: aggregation}).reset_index()
                    grouped_df = grouped_df.sort_values(y_axis, ascending=False).head(top_n)
                    fig = px.bar(grouped_df, x='District', y=y_axis, color=x_axis,
                                 labels={y_axis: f'{y_axis} ({aggregation})', x_axis: f'{x_axis} ({aggregation})'},
                                 title=f'Top {top_n} Districts in {selected_state} by {y_axis} ({aggregation})',
                                 width=1200, height=700)
                
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig)
                
                # Modified download button code
                btn = st.download_button(
                    label="Download graph",
                    data=export_plot(fig),
                    file_name="bar_chart.png",
                    mime="image/png"
                )
           
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
        "Bar Chart": india_bar_chart,
        "Scatter Plot": india_scatter_plot,
        "Data Summary": data_summary
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Select a Page", options=list(pages.keys()))
    pages[selected_page]()

else:
    st.error("Unable to load data. Please check your data file and try again.")

def export_plot(fig):
    try:
        img_bytes = fig.to_image(format="png")
        return img_bytes
    except ValueError:
        # Fallback to SVG if PNG export fails
        svg_bytes = fig.to_image(format="svg")
        return svg_bytes
