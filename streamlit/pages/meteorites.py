import streamlit as st
import pandas as pd
import pydeck as pdk
import os

@st.cache_data
def from_data_file(filename):
    """Load data from a CSV file and return it as a DataFrame."""
    return pd.read_csv(filename)

data_file_path = 'datasets/Meteorite_Landings.csv'

if os.path.exists(data_file_path):
    df = from_data_file(data_file_path)
    df.rename(columns={'reclat': 'lat', 'reclong': 'lon'}, inplace=True)
    df = df[(df['lat'] != 0) & (df['lon'] != 0)].dropna(subset=['lat', 'lon'])
else:
    st.error(f"Dataset not found at {data_file_path}. Please check the file path.")
    df = pd.DataFrame()  # Provide an empty DataFrame as a fallback

if not df.empty:
    st.header("Meteorite Landings Data")
    st.write("Moving the map may be a bit slow due to the large dataset.")
    st.write("The tooltip shows the name, mass, and year of the meteorite.")

    df['normalized_mass'] = df['mass (g)'].apply(lambda x: min(x, 100000) / 100)

    try: 
        ALL_LAYERS = {
            "Meteorite Landings (Mass-Scaled Scatterplot)": pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="normalized_mass",  # Fixed radius in meters
                radius_scale=0.5,   # Increased scale
                radius_min_pixels=2,
                radius_max_pixels=50,
                pickable=True
            ),
            "Meteorite Landings (Heatmap)": pdk.Layer(
                "HexagonLayer",
                data=df,
                get_position=["lon", "lat"],
                radius=10000,
                elevation_scale=50,
                pickable=True,
                extruded=True
            ),
        }

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
    except Exception as e:
        st.error(f"Error loading layers: {e}")
else:
    st.write("No data available to display on the map.")