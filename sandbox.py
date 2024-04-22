import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from scipy.stats import weibull_min
import requests


def main():
    st.title("Wind analysis")

    option = st.selectbox(
    "What area do you want to analyze?",
    ("Utsira Nord", "Sørlige Nordsjø II"),index=None, placeholder="Select area...",)
    st.write('You selected:', option)
    
    if option == 'Utsira Nord':
        latitude, longitude = 59.48222, 4.67361
    elif option == 'Sørlige Nordsjø II':
        latitude, longitude = 56.82333, 4.34666

    # Capture start and end dates from user input
    start_date_formatted = 20180101
    end_date_formatted = 20230101

    # Button to trigger wind analysis
    if st.button("Submit"):
        # Perform wind analysis
        error = perform_wind_analysis(option, latitude, longitude, start_date_formatted, end_date_formatted)
        if error:
            st.error(f"An error occurred: {error}")
        else:
            st.success("Wind analysis completed successfully!")
            # Display wind analysis results...
    
    # Create a default map centered at Oslo
    m = folium.Map(location=[59.0, 5.11], zoom_start=6)

    #Markerer Utsira Nord
    utsira_koordinater = [
    (59.4480556, 4.2691667),
    (59.0694444, 4.4075),
    (59.105, 4.8122222),
    (59.4822222, 4.6736111),
    (59.4480556, 4.2691667),]

    SNii_koordinater = [
    (56.8233333,4.3466667),
    (57.0933333,5.1680556),
    (56.7380556,5.4975),
    (56.5916667,5.0336111),
    (56.4838889,4.6413889),
    (56.8233333,4.3466667),]

    folium.PolyLine(utsira_koordinater, tooltip="Utsira Nord").add_to(m)
    folium.PolyLine(SNii_koordinater, tooltip="Sørlige Norsjø II").add_to(m)

    # Add a click event handler to the map
    m.add_child(folium.ClickForMarker(popup='Latitude: {lat}, Longitude: {lon}'))
    m.add_child(folium.ClickForLatLng())

    folium_static(m)


# Function to perform wind analysis
def perform_wind_analysis(option, latitude, longitude, start_date_formatted, end_date_formatted):
    # Construct URL for API request
    url = f'https://power.larc.nasa.gov/api/temporal/daily/point?start={start_date_formatted}&end={end_date_formatted}&latitude={latitude}&longitude={longitude}&community=RE&parameters=WD50M,WS50M&user=DAVE&format=CSV'

    # API request
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
    except requests.exceptions.RequestException as e:
        return None, None, None, e

    # Check if the response contains data
    if not response.content:
        return None, None, None, "No data returned from the API."

    # Extract wind data
    wind_data_by_direction = [[] for _ in range(12)]
    wind_speeds = []
    wind_directions = []
    for line in response.text.split('\n')[11:]:
        if line.strip() and not line.startswith("-"):
            data = line.strip().split(",")
            if len(data) >= 5:
                wind_speed = float(data[-1])
                wind_direction = float(data[-2])
                wind_speeds.append(wind_speed)
                wind_directions.append(wind_direction)
                direction_group_index = int(wind_direction // 30)
                wind_data_by_direction[direction_group_index].append((wind_speed, wind_direction))

    def plot_wind_rose(wind_directions, wind_speeds, latitude, longitude):
        fig, ax = plt.subplots(subplot_kw={'projection': 'windrose'})
        ax.bar(wind_directions, wind_speeds, normed=True, opening=1, edgecolor='black', lw=0.3, nsector=36, bins =11)
        ax.set_xticklabels(['E', '45°', 'N', '315°', 'W', '225°', 'S', '135°'])

        ax.legend(title='Wind Speed (m/s)', title_fontsize=10, fontsize=8, bbox_to_anchor=(1.1, 0.40), shadow=True, frameon=True, edgecolor='black', facecolor='lightgrey')
        ax.set_title(f'Wind Rose for {option}', fontsize=9.5, loc='center')
        
        return fig

    fig = plot_wind_rose(np.array(wind_directions) % 360, np.array(wind_speeds), latitude, longitude)
    st.pyplot(fig)


    # Total sammenlagt Weibull Graph for alle sektorene
    shape, loc, scale = weibull_min.fit(wind_speeds, floc=0)
    st.write("Shape parameter (k):", shape)
    st.write("Scale parameter (c):", scale)
    x = np.linspace(0, max(wind_speeds), 100)
    weibull_pdf = weibull_min.pdf(x, shape, loc, scale)


    fig2, ax2 = plt.subplots()
    ax2.plot(x, weibull_pdf, label='Weibull PDF')
    ax2.hist(wind_speeds, bins=11, density=True)
    ax2.axvline(np.mean(wind_speeds), color='r', linestyle='--', label=f'Average Wind Speed: {np.mean(wind_speeds):.2f} m/s')
    ax2.set_xlabel('Wind Speed (m/s)')
    ax2.set_ylabel('Probability Density')
    ax2.set_title((f'Weibull Graph for all wind sectors at {option}'))
    ax2.legend()
    st.pyplot(fig2)


    shape_scale= [] #Denne inneholder alle shapes og scales for de 12 sektorene. 
    #Starter med sektor 1 (tilsvarer 0-29 grader), deretter sektor 2 (tilsvarer 30-59 grader) osv...

    # Plot sectors Weibull graph
    fig3, ax3 = plt.subplots(figsize=(8,4.5))
    for i, wind_data in enumerate(wind_data_by_direction):
        wind_speeds_group = [data[0] for data in wind_data]
        shape, loc, scale = weibull_min.fit(wind_speeds_group, floc=0)
        x = np.linspace(0, max(wind_speeds_group), 100)
        weibull_pdf = weibull_min.pdf(x, shape, loc, scale)
        ax3.plot(x, weibull_pdf, label=f'{(i * 30)} to {((i + 1) * 30) % 360} degrees')
        
        # Store shape and scale parameters in the list as tuples
        shape_scale.append((shape, scale))
        #print(f"Jonas print{shape_scale}")
        #print("")
        #print("")

    #data_dict = {key: value for key, value in shape_scale}
    #df = pd.DataFrame(data_dict)

    # Display the table in the sidebar

    df = pd.DataFrame(shape_scale, columns=["Shape", "Scale"])
    st.sidebar.title('Weibull Factors for each wind sector')
    df.index = [f"{i * 30}-{(i + 1) * 30} degrees" for i in range(len(df))]
    st.sidebar.table(df)


    ax3.set_xlabel('Wind Speed (m/s)')
    ax3.set_ylabel('Probability Density')
    ax3.set_title((f'Weibull Graph for each wind sector at {option}'))
    ax3.legend()
    st.pyplot(fig3)    

    # Print shape and scale parameters as a list of tuples
    print("Shape and Scale Parameters for each wind sector:")
    for i, (shape, scale) in enumerate(shape_scale):
        print(f"Sector {(i + 1)} ({(i * 30)} to {((i + 1) * 30) % 360} degrees):")
        print("Shape parameter (k):", shape)
        print("Scale parameter (c):", scale)
        print()

    pass
    

if __name__ == "__main__":
    main()

# streamlit run c:/Users/PureR/Desktop/Bachelor/sandbox.py
