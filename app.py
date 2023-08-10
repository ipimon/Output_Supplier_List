import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt


def set_css():
    # Load custom CSS
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call the set_css function to apply the custom styles
set_css()

# Load the shapefile of Bangladesh's administrative boundaries
shapefile_path = "path_to_your_shapefile/bangladesh_admin_boundaries.shp"  # Replace with the actual file path
gdf = gpd.read_file(shapefile_path)

# Set the initial center of the map to Bangladesh
initial_lat = 23.6850
initial_lon = 90.3563
initial_zoom = 6

# Streamlit app layout
st.title("Bangladesh Map")
st.write("Displaying Bangladesh's administrative boundaries.")

# Display the map using Streamlit
st.pydeck_chart(
    {
        "viewport": {"latitude": initial_lat, "longitude": initial_lon, "zoom": initial_zoom},
        "layers": [
            {
                "data": gdf,
                "type": "GeoJsonLayer",
                "getFillColor": [255, 0, 0, 100],
                "getLineColor": [0, 0, 0],
                "stroked": True,
                "lineWidthScale": 5,
                "filled": True,
                "lineWidthMinPixels": 2,
            }
        ],
    }
)

# Optional: Display additional information about the administrative boundaries
if st.checkbox("Show administrative boundary details"):
    st.dataframe(gdf)

# Show a legend
st.subheader("Legend")
st.write("Red color represents the administrative boundaries.")

# Optional: Display the map using Geopandas and Matplotlib (may not be interactive)
# plt.figure(figsize=(10, 10))
# gdf.plot(ax=plt.gca(), color='red')
# plt.title("Bangladesh Map")
# st.pyplot(plt)
