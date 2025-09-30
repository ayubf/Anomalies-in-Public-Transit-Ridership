import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Anomalies in Public Transit Ridership",
    page_icon=":light_rail:"
)

header_img = Image.open("data/images/featureheader_busandtrain_washington.jpg")
st.image(header_img, caption="A CTA Bus and Train. Source: Transit Chicago / CTA", use_container_width=True)

nyc_ridership_data = pd.read_csv("data/processed/nyc_ridership_data.csv")
chicago_ridership_data = pd.read_csv("data/processed/chicago_ridership_data.csv")
dc_ridership_data = pd.read_csv("data/processed/dc_ridership_data.csv")

nyc_average_ridership = nyc_ridership_data["total_rides"].mean()
chicago_average_ridership = chicago_ridership_data["total_rides"].mean()
dc_average_ridership = dc_ridership_data["total_rides"].mean()

city_to_df = {
    "New York City": nyc_ridership_data,
    "Chicago": chicago_ridership_data,
    "Washington D.C": dc_ridership_data
}

city_to_avg_ridership = {
    "New York City": nyc_average_ridership,
    "Chicago": chicago_average_ridership,
    "Washington D.C": dc_average_ridership
}

"""

# Anomalies in Public Transit Ridership
##### *By Ayub Farah*
Public transit in the United States has a long history: according to the Federal Transit Administration, the first publicly operated ferry carried passengers 
between Chelsea and Boston as early as 1630, and the first subways and cable rail lines appeared in the mid- to late-1800s. After World War II, the rise of 
automobile ownership shifted much investment toward highways, often at the expense of urban transit systems. In recent years, however, many cities have renewed 
focus on developing reliable and effective mass transit.

In this project, we explore the expected versus observed effects of selected events on public transit ridership in three major U.S. cities, 
examining how holidays, systemic shocks, other disruptions, and city and transit authority responses influence usage patterns. 

## Data and Methods

For this project, we will focus on three major U.S cities: New York City, Chicago and Washington D.C. These are the American
cities with the most used public transit systems. We want to focus on a few events that we can separate into two categories. 
The first category is for major holidays: Christmas, Thanksgiving and New Year's. With respect to this category we will be looking at average ridership in a three 
day window centered around the holiday date for each holiday to account for delayed responses. The second category is for extraordinary periods. These are events that last 
for months at a time and to account for delayed responses here we will consider windows of a week before and after the approximate start and end date for each period. 


The ridership data for this project come from the [New York State Open Data Program](https://data.ny.gov/dataset/NYS-Open-Data-Program-Overview/7ruf-yihe/about_data), 
the [NYC Open Data Program](https://opendata.cityofnewyork.us/overview/), the [Chicago Data Portal](https://data.cityofchicago.org/), 
and the [Washington Metropolitan Area Transit Authority](https://www.wmata.com/about/index.cfm). To standardize the analysis across cities, we define a schema that will give us 
the information needed: the date and total ridership per day. 

"""

st.code(
    """
Target schema:
- date: observation date (MM/DD/YYYY)
- total_rides: total daily ridership""",
    language="md"
)


"""
The datasets available through the source portals allowed for filtering and aggregation before download. Specifically, to keep the study consistent, 
we have to consider a window where all dates in the datasets overlap, so we cut off from a minimum start to a minimum end date. 

The CTA (Chicago Transit Authority) ridership dataset already includes a `total_rides` column, but the `Date` column needed renaming. 
Similarly, the WMATA (Washington Metropolitan Area Transit Authority) dataset has a `Grand Total` column, though the `Date` column used a different format. 
For both the CTA and WMATA datasets, the number of total rides is in the form of a string and some include commas, so conversion was needed.
New York City's transit system differs from the other two cities because a significant portion is made up of ferry lines. 
For this reason, we combine ridership data from three separate datasets: one for the MTA (bus, subway, etc.) and two for the NYC and Staten Island ferries.

Below is the preprocessing code:

"""

with open('data/scripts/preprocess.py', 'r') as f: preprocessing_script = f.read()

st.code(preprocessing_script, language="python")

"""

## Ridership During Major Holidays

Christmas, Thanksgiving, and New Year's make up three of the four first federal holidays created in 1870. Almost all schools and government workplaces are closed in the duration 
of a federal holiday and countless private sector businesses observe these three holidays. During these holidays families will often gather around, people travel to see ther loved ones, and 
there are public events like parades or fireworks shows. 

Since transit authorities are public ininstitutions, this means that their offices are closed during federal holidays. Still, transit services usually do run but normally under
reduced hours. New York City hosts the Macy's Thanksgiving Day Parade as well as New Year's Eve festivities in Times Square which lead to street closures and other measures that 
might affect transit ridership. Washington, D.C. is the seat of the U.S. government, so a significant share of the workforce is employed in the public sector or in public-sector-adjacent roles.
This means that more people in this city will get the day off on a federal holiday than average. 

The expectations for ridership numbers for these holidays is that  New York City will see the sharpest decrease, followed by Washington D.C and then Chicago. 
The table below shows ridership for each holiday expressed as a percent change from the overall average.
"""

holiday_dates = [
    ("11/26", "11/27/", "11/28"),
    ("12/24", "12/25", "12/26"), 
    ("12/31", "01/01", "01/02")
]


holiday_dict = {
    "Cities": ["New York City", "Chicago", "Washington D.C"],
    "Thanksgiving Percent Change": [],
    "Christmas Percent Change": [],
    "New Year's Percent Change": []
}

def percent_change_from_avg(df, holiday_ind, avg):
    return f"{ round((df.loc[ df['date'].str.startswith(holiday_dates[holiday_ind]), 'total_rides'].mean() - avg) / avg * 100) }%"


for city in holiday_dict["Cities"]:
    city_df = city_to_df[city]
    avg_ridership = city_to_avg_ridership[city]

    holiday_dict["Thanksgiving Percent Change"].append(percent_change_from_avg(city_df, 0, avg_ridership) )
    holiday_dict["Christmas Percent Change"].append(percent_change_from_avg(city_df, 1, avg_ridership))
    holiday_dict["New Year's Percent Change"].append(percent_change_from_avg(city_df, 2, avg_ridership))

st.dataframe(holiday_dict)

"""

The results show that New York City has the sharpest decrease in ridership as expected. What's interesting is that Chicago and Washington D.C are very close 
in percent changes per holiday, despite the larger share of public sector or public sector adjacent workers in Washington D.C.

"""