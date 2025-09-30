import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Anomalies in Public Transit Ridership",
    page_icon=":light_rail:"
)

header_img = Image.open("data/images/featureheader_busandtrain_washington.jpg")
st.image(header_img, caption="A CTA Bus and Train. Source: Transit Chicago / CTA", use_container_width=True)

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
The first category is for major holidays: Christmas, Thanksgiving and New Years. With respect to this category we will be looking at average ridership in a three 
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

The CTA (Chicago Transit Authority) ridership dataset already includes a `total_rides` column, so only the `Date` column needed renaming. 
Similarly, the WMATA (Washington Metropolitan Area Transit Authority) dataset has a `Grand Total` column, though the `Date` column used a different format. 
New York City's transit system differs from the other two cities because a significant portion is made up of ferry lines. 
For this reason, we combine ridership data from three separate datasets: one for the MTA (bus, subway, etc.) and two for the NYC and Staten Island ferries.

Below is the preprocessing code:

"""

with open('data/scripts/preprocess.py', 'r') as f: preprocessing_script = f.read()

st.code(preprocessing_script, language="python")
