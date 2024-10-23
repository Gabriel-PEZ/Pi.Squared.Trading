# Libraries

import streamlit as st
import geopandas as gpd
import yfinance as yf
import pandas as pd
import pydeck as pdk

# Load world shape data using GeoPandas
@st.cache
def load_world_data():
    return gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Fetch companies for the selected country
def fetch_companies_by_country(country):
    # Example: For simplicity, we'll just use a static list for each country.
    # In a real-world scenario, you can use an API (like Yahoo Finance or a custom dataset).
    companies_data = {
        "United States": ["Apple", "Google", "Microsoft", "Amazon"],
        "Canada": ["Shopify", "Royal Bank of Canada", "Enbridge"],
        "Germany": ["Volkswagen", "Siemens", "Deutsche Bank"],
        "Japan": ["Toyota", "Sony", "Nintendo"],
    }
    return companies_data.get(country, [])

# Main function to handle UI
def main():
    st.title("World Stock Market Selector")

    # Load world map data
    world = load_world_data()

    # Display the map using PyDeck
    st.subheader("Select a country by clicking on it:")

    # Create a PyDeck map for user interaction
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=world,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_fill_color="[200, 30, 0, 160]",
        get_line_color=[255, 255, 255],
    )

    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1)

    # Display the map
    r = pdk.Deck(layers=[geojson_layer], initial_view_state=view_state, tooltip={"text": "{name}"})
    selected_data = st.pydeck_chart(r)

    # If user clicks on the map, show the selected country and companies
    if selected_data is not None:
        st.write("You selected: ", selected_data)  # `selected_data` needs to map the click event to a country

        # Example to map selection back to country, this would be based on real data from the map click event
        selected_country = selected_data.get('name', 'No Country Selected')  # This would be parsed from event

        st.write(f"Companies in {selected_country}:")
        
        # Fetch and display companies
        companies = fetch_companies_by_country(selected_country)
        if companies:
            st.write(companies)
        else:
            st.write("No company data available for this country.")

if __name__ == '__main__':
    main()