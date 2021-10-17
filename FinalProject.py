import streamlit as st
from streamlit_observable import observable
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from matplotlib import cm
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import plotly.express as px
import plotly.figure_factory as pff
plt.style.use('plotstyles/DGplots.mplstyle')

##### DATA IMPORTING SECTION #####
# Import all relevant datasets in this section so they'll be accessible in all sections

@st.cache
def import_data():
    lowNet = pd.read_csv('Datasets/smallestNetOutflows.csv').rename(columns={'Unnamed: 0':'FIPS'})
    highNet = pd.read_csv('Datasets/largestNetOutflows.csv').rename(columns={'Unnamed: 0':'FIPS'})
    lowNet['FIPS'] = ["%05d" % elem for elem in lowNet['FIPS']]
    highNet['FIPS'] = ["%05d" % elem for elem in highNet['FIPS']]
    lowFIPS = lowNet['FIPS'].to_list()
    highFIPS = highNet['FIPS'].to_list()

    popmig = pd.read_csv('Datasets/population_migration.csv')
    popmig['FIPS'] = ["%05d" % elem for elem in popmig['FIPS']]
    popmig['dest_FIPS'] = ["%05d" % elem for elem in popmig['dest_FIPS']]

    aqis = pd.read_csv('Datasets/AQI_by_County.csv')
    aqis['FIPS'] = ["%05d" % elem for elem in aqis['FIPS']]

    return lowFIPS,highFIPS,popmig,aqis

lowFIPS,highFIPS,popmig,aqis = import_data()


##### END DATA IMPORTING SECTION #####

#### TITE AND HEADER ####
# Title and header
st.markdown(''' # Landscape of the New America: How the US population will be redistributed in 2050 ''')
st.markdown(''' ## Team 24 ''')
st.markdown('''Danah Park | Devi Ganapathi | Emily Wang | Gabrielle Cardoza | Irene Alisjahbana | Liz Peterson | Noemi Valdez ''')

section = st.sidebar.selectbox("Outline",("Project Description","Datasets","Exploratory Data Analysis","Model Building","Results","Conclusions"))

if section == "Project Description":
    st.markdown(''' 
    ## Project Description
    
    ### Problem Overview
    
    As the United States grows in population, and becomes more racially and ethnically diverse, the role of how demographics &     migration patterns play into our future population make up has the ability to influence our countries socioeconomic communities     and climate change impacts. Our research goal with our model is to predict how the US social landscape and redistribution of     populations will look in the next 30 years using population estimates, population migration,climate variables such as AQI &     natural disaster & social demographic variables specifically housing, economic and income data. 
    
    ### Specific Issue
    
    We will examine the extent of population migration on our social demographic variables using current population datasets and     their effects on the US population demographics look in 2050. Additionally, we will analyze demographics with the purpose to     find new social economic trends by identifying population numbers over time. For our project we are focusing on the impact of     population migration and size on demographic shifts. 
    
    ### Problem Importance
    
    It is important that we as a society have a general idea on what the population will look like in a few decades. Population &     demographic changes affect not only our voting demographic that could sway elections, it can also predict new urban area,     housing markets, inform climate researches how many people will be affected by global warming adverse effects in the future, if     we will have the proportional educational resources in that area and assist business on where the future generations will be     nesting.
    
    #### Potential Audiences: 
    
    - Government influencers: Having the ability to forecast how the population will look in certain states demographically could heavily impact voting outcomes, redistricting & the type of candidates that might succeed. Demographics in a state for example play a big role if a purple state swings to red or blue. 
    - Climate Research: Using our model to look deeper where populations are growing in juxtaposition where climate change factors such as air quality, water supply, rising temperatures are being greatly impacted has the ability to possibly predict how many people could be affected with certain climate crises in the future.
    - Real estate: Being aware of where population hubs will be growing could help inform future housing supply, housing cost & even possibly if certain areas seen as rural right now will transition to more urban in the near future.
    - Education: As our population in the US now tends to have children at an older age, some questions educators would want to know are: what will birth rates look like in the future? What areas will need more schools or teachers? What areas will have less children and might not need extra funding? 
    - Business: Finding out what, where & how demographics have shifted in the US, will help marketers scope out audiences, refine product targeting & plan out advertising buys in the future. In parallel being able to see where the younger populations will inhabit will also help companies make choices on where to open offices to boost hiring. 

    ''')

elif section == "Datasets":

    # Make table with all data sources - cached
    @st.cache()
    def make_dataset_table():
        datasets = [dict(Variable='Population Migration', Source="IRS", URL="https://www.irs.gov/statistics/soi-tax-stats-migration-data", Details="Migration data (inflows and outflows) by county, estimated annually (1991-2019)"),
        dict(Variable='Population', Source="US Census", URL="https://www2.census.gov/programs-surveys/popest/datasets/", Details="Population data by county, broken down by age, race and gender, estimated annually (1970-2020)"),
        dict(Variable='Birth Data', Source="CDC", URL="https://wonder.cdc.gov/Natality.html", Details="Births occurring within the US to US residents, with county of residence. Derived from birth certificates issued in (1995-2019)"),
        dict(Variable='Natural Disasters', Source="FEMA", URL="https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2", Details="Natural disasters by date, type of incident, programs declared, and county going back to 1950s"),
        dict(Variable='AQI', Source="EPA", URL="https://aqs.epa.gov/aqsweb/airdata/download_files.html#Annual" , Details="Natural disasters by date, type of incident, programs declared, and county going back to 1950s"),
        dict(Variable='Employment', Source="BEA", URL="https://apps.bea.gov/iTable/iTable.cfm?reqid=70&step=1&acrdn=6" , Details="Employment (total number of full time and part time jobs) by County from 1969-2019"),
        dict(Variable='Income', Source="BEA", URL="https://apps.bea.gov/iTable/iTable.cfm?reqid=70&step=1&acrdn=6" , Details="Personal Income and Population by County from 1969-2019"),
        dict(Variable='HPI', Source="FHFA", URL="https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_AT_BDL_county.xlsx" ,Details="Housing Price Index by County from 1986 to 2020, with both 1990 and 2000 base"),
        dict(Variable='FMR', Source="HUD", URL="https://www.huduser.gov/portal/dataset/fmr-api.html" , Details="Fair Market Rent (40th Percentile) by County from 2000-2022")]

        dataset_table = pd.DataFrame(datasets)

        def make_clickable(url, name):
            return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

        dataset_table['Source'] = dataset_table.apply(lambda x: make_clickable(x['URL'], x['Source']), axis=1)

        dataset_table = dataset_table[['Variable','Source','Details']]

        return dataset_table

    # Run the function to make the dataset table and display it
    dataset_table = make_dataset_table()
    st.write(dataset_table.to_html(escape=False,index=False),unsafe_allow_html=True)

    st.markdown('''  &nbsp;  
    ### Population Migration
    The population migration dataset was obtained from the IRS. The Outflow dataset contains information of the estimated number of individuals that moved from county A to county B. The dataset was available on a yearly basis from 1991-2019. However, because 1991 and 1992 had very different formats, we decided to use data from 1993-2019. We combined the yearly datasets into one CSV file for use in our model. The columns include the origin state and county, the destination state and county, the number of individuals that moved from origin to destination, and the aggregated gross income of all the individuals. If we want to obtain the number of individuals that moved into a certain county, then we would sum the number of individuals that had a destination county of interest. 

    ### Population
    The total population dataset was downloaded from the US Census. The data was available per year per county, with years grouped in 10 year increments. Demographic data was also available in these datasets, but the demographic categories were not consistent decade to decade. The datasets were also structured differently decade to decade so combining the datasets was challenging. The totals of the populations summed over all demographics were used to get the total population of each county per year. This dataset will be used as a dependent variable if we want to explore beyond net migration outflows for each county.

    ### AQI
    The AQI dataset was downloaded from the United States Environmental Protection Agency (aqs.epa.gov). The AQI datasets are available by county by year, with a separate file for each year. All available datasets were downloaded and concatenated using pandas. This process was straightforward because all years had the same reported metrics. The data was then grouped by the five digit Federal Information Processing Standard (FIPS) code, which is a unique identifier for each county in the US. From this dataset, the median AQI was used to perform further analysis.

    ### Economic and Income/Population
    Data for total Full-time and Part-time Employment as well as data for Personal Income were downloaded from the Bureau of Economic Analysis (https://www.bea.gov/) for the years 1969 to 2019. This data is available at a county-by-county level. Personal Income data includes the total personal income for all residents of a county, the population of that county, and per capita personal income. 

    ### Disasters
    The Disasters Dataset was downloaded from the U.S. Department of Homeland Security FEMA website. This data set states the specific states and counties in which disasters have occured (whether natural or man-made). The data goes back to 1953 and captures up to the year 2021. One of the key variables we looked at was “incidentType” to understand what type of emergency had been declared and how many types that specific disaster had occurred. This can allow us to dive deeper into analyzing what areas might be the most affected by a specific type of disaster and focus on what population migration looks like in that region. 

    ### Housing
    The Housing Price Index (HPI) dataset was downloaded from the Fair Housing Finance Agency (FHFA) website. Data is available by county and by year from 1986-2019 with HPIs referenced to housing prices in 1986. Fair Market Rent (FMR) data was downloaded from the Department of Housing and Urban Development (HUD) website via their Office of Policy Development and Research (PD&R). This dataset includes the 40th percentile rental rates by county and by year for Studio, 1, 2, 3, and 4 Bedroom units from 2004-2021.
    ''')
    
elif section == "Exploratory Data Analysis":
    
    st.markdown('''
    ### Visualizing Trends for Counties
    To visualize the trends in the data over time, we chose two subsets of counties to look at. The first subset is the group of counties with the highest net outflows in population, as observed in 2018 (to avoid COVID-19 related effects). The second subset is the group of counties with the lowest net outflows in population (highest net inflows), also as observed in 2018. 
    ''')

    #### START AQI TIME PLOTS ####
    # Counties with lowest net migration outflow
    start_year,end_year = st.select_slider(label='Year Range to Plot',options=np.arange(1993,2020,1),value=(1993,2019))
    colors = cm.viridis(np.linspace(0,1,len(lowFIPS)))
    fig,ax = plt.subplots()
    i = 0
    for fips in lowFIPS:
      x = aqis[aqis['FIPS']==fips]
      x = x[x['year'].isin(np.arange(start_year,end_year,1))]['year']
      y = aqis[aqis['FIPS']==fips]
      y = y[y['year'].isin(np.arange(start_year,end_year,1))]['Median AQI']
      plt.plot(x,y,color=colors[i])
      i += 1
    plt.xlabel('Year')
    plt.ylabel('Median AQI')
    plt.title('Counties with Highest Net Inflows')
    
    st.pyplot(fig)

# Counties with highest net migration outflow
    if st.button('Plot AQIs for Counties with Highest Net Migration Outflow in 2018'):
        colors = cm.viridis(np.linspace(0,1,len(highFIPS)))
        i = 0
        fig,ax = plt.subplots()
        for fips in highFIPS:
          x = aqis[aqis['FIPS']==fips]['year']
          y = aqis[aqis['FIPS']==fips]['Median AQI']
          plt.plot(x,y,color=colors[i])
          i += 1
        plt.xlabel('Year')
        plt.ylabel('Median AQI')
        plt.title('Counties with Highest Net Outflows')
        
        st.pyplot(fig)

    #### END AQI TIME PLOTS ####
     

elif section == "Results":
        
     #### AQI Heat Map ####
    year = st.slider(label='Year',min_value = 1993, max_value = 2020)
    aqi_map = aqis[aqis['year']==year]
    #  fips = aqi_map['FIPS']
    
    st.write(len(aqi_map[aqi_map['State']=='Wyoming']))
    
    fig = px.choropleth(aqi_map,geojson=counties, locations="FIPS",color='Median AQI',hover_name="County",color_continuous_scale="Viridis",range_color=(0,250),scope="usa",labels={'Median AQI':'Median AQI'})
    # fig.add_scattergeo(geojson=counties,locations=)
    
    # fig = pff.create_choropleth(fips = aqi_map['FIPS'],values=aqi_map['Median AQI'])
    
    st.write(fig)

 
    components.html(
        """
        <div id="observablehq-a70836fb">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/map_2019.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-a70836fb .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-a70836fb .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-a70836fb .observablehq-update")();
          });
        </script>
        """, height = 600,)