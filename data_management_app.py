import streamlit as st
import pandas as pd
import folium

# List of stored user credentials
users = {
    "imon": "ip10",
    "Tahmid": "TahMid2023",
    "ip": "1017"
}

def authenticate(username, password):
    return users.get(username) == password

# Function to set up the dashboard
def show_dashboard():
    st.write('<div class="icon-container"><img src="https://seeklogo.com/images/I/i-farmer-asia-bd-logo-848E96BFDD-seeklogo.com.png"></div>', unsafe_allow_html=True)
    # Get the username from session state
    username = st.session_state.username

    # Display the username in the dashboard
    st.header(f"Hello, :orange[{username}]!")
    st.title("Welcome to :green[iFarmer] Dashboard")

    # Load and display supplier data
    df = get_data()
    st.header("All Supplier Data")

    # Sidebar filtering options
    divisions = df['division'].drop_duplicates()
    division_choice = st.sidebar.selectbox('Select your Division:', [''] + list(divisions))

    if division_choice:
        st.subheader(f"Data for Division: :green[{division_choice}]")
        division_data = df[df["division"] == division_choice]

        districts = division_data["district"].drop_duplicates()
        district_choice = st.sidebar.selectbox('Select District:', [''] + list(districts))

        if district_choice:
            st.subheader(f"Data for District: :green[{district_choice}]")
            district_data = division_data[df["district"] == district_choice]

            upazilas = district_data["upazila"].drop_duplicates()
            upazila_choice = st.sidebar.selectbox('Select Upazila:', [''] + list(upazilas))

            if upazila_choice:
                st.subheader(f"Data for Upazila: :green[{upazila_choice}]")
                upazila_data = district_data[df["upazila"] == upazila_choice]
                st.dataframe(upazila_data)
                # Add the "Download" button for the selected data
                if st.button("Download Data"):
                    download_data(upazila_data)
                # Create a map with markers for each location
                show_map = st.checkbox("Show Map")
                if show_map:
                    map_upazila = folium.Map(location=[upazila_data['latitude'].mean(), upazila_data['longitude'].mean()], zoom_start=12)
                    for _, row in upazila_data.iterrows():
                        folium.Marker(
                            location=[row['latitude'], row['longitude']],
                            popup=row['name'],
                            tooltip=row['name'],  # Tooltip for the marker
                            icon=folium.Icon(color='green', icon='leaf')
                        ).add_to(map_upazila)
                    folium.TileLayer('openstreetmap').add_to(map_upazila)
                    folium.TileLayer('stamentoner', name='stamentoner').add_to(map_upazila)
                    folium.LayerControl().add_to(map_upazila)
                    st.write(map_upazila)

            else:
                st.dataframe(district_data)
                # Add the "Download" button for the selected data
                if st.button("Download Data"):
                    download_data(district_data)
                # Create a map with markers for each location
                show_map = st.checkbox("Show Map")
                if show_map:
                    map_district = folium.Map(location=[district_data['latitude'].mean(), district_data['longitude'].mean()], zoom_start=10)
                    for _, row in district_data.iterrows():
                        folium.Marker(
                            location=[row['latitude'], row['longitude']],
                            popup=row['name'],
                            tooltip=row['name'],  # Tooltip for the marker
                            icon=folium.Icon(color='blue', icon='info-sign')
                        ).add_to(map_district)
                    folium.TileLayer('Stamen Terrain').add_to(map_district)
                    folium.TileLayer('OpenStreetMap').add_to(map_district)
                    folium.LayerControl().add_to(map_district)
                    st.write(map_district)

        else:
            st.dataframe(division_data)
            # Add the "Download" button for the selected data
            if st.button("Download Data"):
                download_data(division_data)
            # Create a map with markers for each location
            show_map = st.checkbox("Show Map")
            if show_map:
                map_division = folium.Map(location=[division_data['latitude'].mean(), division_data['longitude'].mean()], zoom_start=8)
                for _, row in division_data.iterrows():
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=row['name'],
                        tooltip=row['name'],  # Tooltip for the marker
                        icon=folium.Icon(color='red', icon='glyphicon-home')
                    ).add_to(map_division)
                folium.TileLayer('OpenStreetMap').add_to(map_division)
                folium.TileLayer('stamentoner', name='stamentoner').add_to(map_division)
                folium.LayerControl().add_to(map_division)
                st.write(map_division)

# Function to download selected data to Excel
def download_data(data):
    # Prompt user to download the data as an Excel file
    data.to_excel("selected_data.xlsx", index=False)
    st.success("Selected data exported to 'selected_data.xlsx'!")

# Function to load data
def get_data():
    path = "suplocation.csv"
    return pd.read_csv(path, index_col=0)

# Main function for the Streamlit app
def main():
    # Check if the user is logged in
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # If the user is not authenticated, display the login page
    if not st.session_state.is_authenticated:
        st.set_page_config(page_title="Supplier Login", page_icon="https://i.ibb.co/SQBK7Sc/ifarmelv.png")
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Check credentials
            if authenticate(username, password):
                st.session_state.is_authenticated = True
                st.session_state.username = username
                st.experimental_rerun()
                show_dashboard()
            else:
                st.error("Invalid username or password. Please try again.")
    else:
        # Call the function to set the page configuration
        st.set_page_config(page_title="Dashboard", layout="wide", page_icon="https://i.ibb.co/SQBK7Sc/ifarmelv.png")  # Set wide layout
        show_dashboard()

if __name__ == "__main__":
    main()
