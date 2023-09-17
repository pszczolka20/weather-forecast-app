import streamlit as st
import plotly.express as px
from backend import get_data

# add title, text input, slider, selectbox, subheader
st.title("Weather Forecast for the Next Days")

place = st.text_input("Place: ")

days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        # Get the temperature/sky condition
        filtered_data = get_data(place, days)
        dates = [dict["dt_txt"] for dict in filtered_data]

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            images = [f"images/{condition.lower()}.png" for condition in sky_conditions]
            st.image(images, dates, width=115)

    except KeyError:
        st.warning("Please enter a valid city", icon="⚠️")