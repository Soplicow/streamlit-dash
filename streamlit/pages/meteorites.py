import streamlit as st
import pandas as pd
import pydeck as pdk
import os

@st.cache_data(show_spinner=False)
def from_data_file(filename):
    try:
        return pd.read_csv(filename)
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return pd.DataFrame()

data_file_path = os.path.join('datasets', 'Meteorite_Landings.csv')

if os.path.exists(data_file_path):
    df = from_data_file(data_file_path)
    df.rename(columns={'reclat': 'lat', 'reclong': 'lon'}, inplace=True)
    df = df[(df['lat'] != 0) & (df['lon'] != 0)].dropna(subset=['lat', 'lon'])
    df['mass (g)'] = pd.to_numeric(df['mass (g)'], errors='coerce').fillna(0)
else:
    st.error(f"Dataset not found at {data_file_path}. Please check the file path.")
    df = pd.DataFrame()

if not df.empty:
    st.header("Meteorite Landings Data")
    st.write("Moving the map may be a bit slow due to the large dataset.")
    st.write("The tooltip shows the name, mass, and year of the meteorite.")

    df['normalized_mass'] = df['mass (g)'].clip(upper=100000) / 100

    # Year filter: slider and manual input
    if 'year' in df.columns:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())

        st.sidebar.markdown("### Filter by Year Range")
        col1, col2 = st.sidebar.columns(2)
        manual_min = col1.number_input("Start Year", min_value=min_year, max_value=max_year, value=min_year, key="manual_min_year")
        manual_max = col2.number_input("End Year", min_value=min_year, max_value=max_year, value=max_year, key="manual_max_year")

        year_range = st.sidebar.slider("Year Range", min_year, max_year, (manual_min, manual_max), key="year_slider")

        # Use the most recent input (manual or slider)
        start_year = min(year_range[0], manual_min)
        end_year = max(year_range[1], manual_max)
        if start_year > end_year:
            st.sidebar.warning("Start year must be less than or equal to end year.")
        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]

    def get_layers(data):
        return {
            "Meteorite Landings (Mass-Scaled Scatterplot)": pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="normalized_mass",
                radius_scale=0.5,
                radius_min_pixels=2,
                radius_max_pixels=50,
                pickable=True
            ),
            "Meteorite Landings (Heatmap)": pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=10000,
                elevation_scale=50,
                pickable=True,
                extruded=True
            ),
        }

    ALL_LAYERS = get_layers(df)
    st.sidebar.title("Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]

    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": df['lat'].mean(),
                    "longitude": df['lon'].mean(),
                    "zoom": 1,
                    "pitch": 50,
                },
                layers=selected_layers,
                tooltip={
                    "html": "<b>Name:</b> {name}<br/>"
                            "<b>Mass:</b> {mass (g)} g<br/>"
                            "<b>Year:</b> {year}",
                    "style": {
                        "backgroundColor": "steelblue",
                        "color": "white"
                    }
                }
            )
        )
    else:
        st.warning("Please select at least one layer above.")
else:
    st.write("No data available to display on the map.")