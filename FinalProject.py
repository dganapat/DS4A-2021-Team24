import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from matplotlib import cm
from urllib.request import urlopen
import json
import statsmodels.api as sm
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import plotly.express as px
import plotly.figure_factory as pff
import matplotlib as mpl
import io
plt.style.use('plotstyles/DGplots.mplstyle')

##### DATA IMPORTING SECTION #####
# Import all relevant datasets in this section so they'll be accessible in all sections

def get_color_dict(df, color_var):
    var1 = df[color_var].drop_duplicates()
    color_array = plt.get_cmap('viridis')(np.linspace(0, 1, num=df[color_var].nunique(), endpoint=True))
    return dict(zip(var1, color_array))

def get_high_low_dfs(df,highNet,lowNet):
    df_highNet = df.loc[df.FIPS.isin(highNet.FIPS.tolist())].copy()
    df_lowNet = df.loc[df.FIPS.isin(lowNet.FIPS.tolist())].copy()
    return df_highNet, df_lowNet

def get_high_low_10_dfs(df,highNet,lowNet):
  highNet_10 = highNet.sort_values('Net Outflow', ascending = False).head(10)
  lowNet_10 = lowNet.sort_values('Net Outflow', ascending = True).head(10)
  df_highNet = df.loc[df.FIPS.isin(highNet_10.FIPS.tolist())].copy()
  df_lowNet = df.loc[df.FIPS.isin(lowNet_10.FIPS.tolist())].copy()
  return df_highNet, df_lowNet

@st.cache(suppress_st_warning=True)
def import_data():
  lowNet = pd.read_csv('Datasets/smallestNetOutflows.csv').rename(columns={'Unnamed: 0':'FIPS'})
  highNet = pd.read_csv('Datasets/largestNetOutflows.csv').rename(columns={'Unnamed: 0':'FIPS'})
  lowFIPS = ["%05d" % elem for elem in lowNet['FIPS']]
  highFIPS = ["%05d" % elem for elem in highNet['FIPS']]

  popmig = pd.read_csv('Datasets/population_migration.csv')
  popmig['FIPS'] = ["%05d" % elem for elem in popmig['FIPS']]
  popmig['dest_FIPS'] = ["%05d" % elem for elem in popmig['dest_FIPS']]

  county_net_out = pd.read_csv('Datasets/county_net_out.csv')

  hpis = pd.read_csv('Datasets/HPI.csv')
  hpis['FIPS'] = ["%05d" % elem for elem in hpis['FIPS']]

  migration_net = pd.read_csv('Datasets/migration_net.csv')

  disaster_types = pd.read_csv('Datasets/disaster_types.csv')
  disaster_migration = pd.read_csv('Datasets/disaster_migration.csv')
  color_dict_years = get_color_dict(disaster_migration, 'year')

  hpi_migration = pd.read_csv('Datasets/hpi_migration.csv')
  income_migration = pd.read_csv('Datasets/income_migration.csv')
  employment_migration = pd.read_csv('Datasets/employment_migration.csv')
  population_migration = pd.read_csv('Datasets/population_migration_eda.csv')
  fmr_migration = pd.read_csv('Datasets/fmr_migration.csv')
  aqi_migration = pd.read_csv('Datasets/aqi_migration.csv')

  return highNet,lowNet,lowFIPS,highFIPS,popmig,county_net_out,hpis,migration_net,disaster_types,disaster_migration,color_dict_years,hpi_migration,income_migration,employment_migration,population_migration,fmr_migration,aqi_migration

highNet,lowNet,lowFIPS,highFIPS,popmig,county_net_out,hpis,migration_net,disaster_types,disaster_migration,color_dict_years,hpi_migration,income_migration,employment_migration,population_migration,fmr_migration,aqi_migration = import_data()
##### END DATA IMPORTING SECTION #####


#### Sidebar Header
st.sidebar.markdown("""
# Landscape of the New America: How domestic migration will redistribute the US population in 2030
## Team 24
Danah Park | Devi Ganapathi | Elizabeth Peterson |  Emily Wang | Gabrielle Cardoza | Irene Alisjahbana  | Noemi Valdez
""")
#### Outline Options for Sidebar
section = st.sidebar.selectbox("Outline",("Executive Summary","Project Description","Datasets","Exploratory Data Analysis","Methodology","Results","Conclusions & Limitations","Supplemental Information"))

#### EXECUTIVE SUMMARY SECTION
if section == "Executive Summary":
  st.markdown(''' # Landscape of the New America: How How domestic migration will redistribute the US population in 2030 
  ## Team 24 
  Danah Park | Devi Ganapathi | Elizabeth Peterson |  Emily Wang | Gabrielle Cardoza | Irene Alisjahbana  | Noemi Valdez
  # Executive Summary
  
  ''')  
  components.html(
          """
        <div id="observablehq-756613fe">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/popmig_proj.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-756613fe .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-756613fe .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-756613fe .observablehq-update")();
          });
        </script>
          """, height = 600,)

#### PROJECT DESCRIPTION SECTION ####
if section == "Project Description":
  #### TITE AND HEADER ####
  # Title and header
  # st.markdown(''' # Landscape of the New America: How How domestic migration will redistribute the US population in 2030 
  # ## Team 24 
  # Danah Park | Devi Ganapathi | Elizabeth Peterson | Emily Wang | Gabrielle Cardoza | Irene Alisjahbana  | Noemi Valdez
  # ''')
    
  st.markdown(''' 
    # Project Description
    
    ### Problem Overview
    
    As the United States grows in population, migration patterns in our future population will influence our country’s socioeconomic communities and the impact of climate change. Our research goal with our model is to predict how the US social landscape and redistribution of populations will look in the next 30 years using population estimates, population migration, climate variables such as natural disasters, and social demographic variables such as housing, economic and income data.  
    
    ### Specific Issue
    
    We will examine the extent of population migration caused by our social demographic variables using current population datasets projected out to 2050.
    
    ### Problem Importance
    
    It is important that we as a society have a general idea of what the population will look like in a few decades. Population & demographic changes affect not only our voting demographic that could sway elections, it can also predict new urban areas, housing markets, required educational resources, and number of people who will be affected by global warming’s adverse effects in the future, along with informing businesses on where the future generations will be nesting.
    
    #### Potential Audiences: 
    
    - Government influencers: Having the ability to forecast how the population will look in certain states demographically could heavily impact voting outcomes, redistricting & the type of candidates that might succeed. Demographics in a state for example play a big role if a purple state swings to red or blue. 
    - Climate Research: Using our model to look deeper where populations are growing in juxtaposition where climate change factors such as air quality, water supply, rising temperatures are being greatly impacted has the ability to possibly predict how many people could be affected by climate crises in the future.
    - Real estate: Being aware of where population hubs will be growing could help inform future housing supply, housing cost & even possibly if certain areas seen as rural right now will transition to more urban in the near future.
    - Education: As our population in the US now tends to have children at an older age, some questions educators would want to know are:  Which areas will need more schools or teachers? Which areas will have less children and might not need extra funding? 
    - Business: Finding out where & how demographics have shifted in the US, will help marketers scope out audiences, refine product targeting & plan out advertising buys in the future. In parallel being able to see where the younger populations will inhabit will also help companies make choices on where to open offices to boost hiring. 

    ''')

#### DATASETS SECTION ####
elif section == "Datasets":
  st.markdown(""" # Datasets """)
  # Make table with all data sources - cached
  @st.cache()
  def make_dataset_table():
      datasets = [dict(Variable='Population Migration', Source="IRS", URL="https://www.irs.gov/statistics/soi-tax-stats-migration-data", Details="Migration data (inflows and outflows) by county, estimated annually (1991-2019)"),
      dict(Variable='Population', Source="US Census", URL="https://www2.census.gov/programs-surveys/popest/datasets/", Details="Population data by county, broken down by age, race and gender, estimated annually (1970-2020)"),
      dict(Variable='Birth Data', Source="CDC", URL="https://wonder.cdc.gov/Natality.html", Details="Births occurring within the US to US residents, with county of residence. Derived from birth certificates issued in (1995-2019)"),
      dict(Variable='Natural Disasters', Source="FEMA", URL="https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2", Details="Natural disasters by date, type of incident, programs declared, and county going back to 1950s"),
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
  st.markdown('''
    We leveraged several publicly available datasets for our project:
    ''')


  dataset_table = make_dataset_table()
  st.write(dataset_table.to_html(escape=False,index=False),unsafe_allow_html=True)

  st.markdown('''  &nbsp;  
  ### Population Migration
  We obtained the population migration dataset from the [IRS](https://www.irs.gov/statistics/soi-tax-stats-migration-data). The Outflow dataset contains information of the estimated number of individuals that moved from county A to county B. The dataset was available on a yearly basis from 1991-2019. However, because 1991 and 1992 had very different formats, we decided to use data from 1993-2019. We combined the yearly datasets into one CSV file for use in our model. The columns include the origin state and county, the destination state and county, the number of individuals that moved from origin to destination, and the aggregated gross income of all the individuals. 

  In our project, we decided to focus on net outflow migration of each county, instead of each origin-destination pair. This was calculated by summing the number of individuals that had an origin county of interest. 

  ### Population
  We downloaded the total population dataset from the [US Census](https://www2.census.gov/programs-surveys/popest/datasets/). The data was available per year per county, with years grouped in 10 year increments. Demographic data was also available in these datasets, but the demographic categories were not consistent decade to decade. The datasets were also structured differently decade to decade so combining the datasets was challenging. We used the totals of the populations summed over all demographics to get the total population of each county per year. This dataset will be used as a dependent variable if we want to explore beyond net migration outflows for each county.

  ### Economic and Income/Population
  We downloaded data for total [Full-time and Part-time Employment](https://apps.bea.gov/iTable/iTable.cfm?reqid=70&step=30&isuri=1&major_area=4&area=xx&year=2019&tableid=33&category=733&area_type=4&year_end=-1&classification=naics&state=xx&statistic=10&yearbegin=-1&unit_of_measure=levels) as well as data for [Personal Income](https://apps.bea.gov/iTable/iTable.cfm?reqid=70&step=30&isuri=1&major_area=4&area=xx&year=2019&tableid=20&category=720&area_type=4&year_end=-1&classification=non-industry&state=xx&statistic=-1&yearbegin=-1&unit_of_measure=levels) from the Bureau of Economic Analysis (https://www.bea.gov/) for the years 1969 to 2019. This data is available at a county-by-county level. Personal Income data includes the total personal income for all residents of a county, the population of that county, and per capita personal income.

  ### Disasters 
  We downloaded the Disasters Dataset from the [U.S. Department of Homeland Security FEMA website](https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2). This data set states the specific states and counties in which disasters have occured (whether natural or man-made). The data goes back to 1953 and captures up to the year 2021. One of the key variables we looked at was “incidentType” to understand what type of emergency had been declared and how many types that specific disaster had occurred. This can allow us to dive deeper into analyzing what areas might be the most affected by a specific type of disaster and focus on what population migration looks like in that region.

  ### Housing
  We downloaded the Housing Price Index (HPI) dataset from the Fair Housing Finance Agency ([FHFA](https://www.fhfa.gov/)) website. Data is available by county and by year from 1986-2019 with HPIs referenced to housing prices in 1986. We downloaded fair Market Rent (FMR) data from the Department of Housing and Urban Development ([HUD](https://www.huduser.gov/portal/datasets/fmr.html)) website via their Office of Policy Development and Research (PD&R). This dataset includes the 40th percentile rental rates by county and by year for Studio, 1, 2, 3, and 4 Bedroom units from 2004-2021. 

    ''')

#### EDA SECTION #### 
elif section == "Exploratory Data Analysis":
  st.markdown('''
  # Exploratory Data Analysis
  ### Visualizing Trends for Counties
  To visualize the trends in the data over time, we chose two subsets of counties to look at. The first subset is the group of counties with the highest net outflows in population, as observed in 2018 (to avoid COVID-19 related effects). The second subset is the group of counties with the lowest net outflows in population (highest net inflows), also as observed in 2018. 
  ''')

  choice = st.selectbox(label="EDA Variables to View",options=["Population Migration","Population","Number of Disasters","Housing Price Index","Income","Employment","All Variables"])

  # Population Migration EDA
  if choice == "Population Migration" or choice == "All Variables":
    st.markdown('''
          ### Population Migration
          ''')

    st.markdown("""We subtracted the total county outflows and inflows to obtain the net outflow number, plotted in the figure below:""")

    components.html("""
        <div id="observablehq-e27ece4f">
      <div class="observablehq-chart"></div>
    </div>
    <script type="module">
      import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
      import define from "https://api.observablehq.com/@ialsjbn/net_migration.js?v=3";
      (new Runtime).module(define, name => {
        if (name === "chart") return Inspector.into("#observablehq-e27ece4f .observablehq-chart")();
      });
    </script>
    """, height = 600)
    st.caption("Net population migration from 1993-2019. Note: hover over a line to see which county it is!")

    st.markdown(""" A positive number indicates that more people move out of the county, whereas a negative number indicates that more people move into the county. From the plot below, we can see that in general, many counties have constant net migration near 0, which means that as many people are moving out, as they are moving in. However, some counties have consistently more people moving out of the county (for example, Los Angeles, CA), while others have consistently more people moving in (for example, Maricopa, AZ). Some counties experience anomalous increases in net outflow or net inflow, such as Cook, IL and Travis, TX.
    """)

    components.html(
            """
            <div id="observablehq-a70836fb">
              <div class="observablehq-viewof-year_select"></div>
              <div class="observablehq-chart"></div>
              <div class="observablehq-update" style="display:none"></div>
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
  st.caption("Note: Click the play button to see how the population migration changes over time! You can also hover over a county to see more information.")
  
  if choice == "Population" or choice == "All Variables":
    # Population EDA
    st.markdown("""
    ### Population
    A heat map of total population is shown below to visualize how population changes by county in time.
    """)

    components.html("""
        <div id="observablehq-ff6b2a54">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/population.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-ff6b2a54 .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-ff6b2a54 .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-ff6b2a54 .observablehq-update")();
          });
        </script>
        """, height = 600)

    st.caption("Note: Click the play button to see how the population numbers changes over time! You can also hover over a county to see more information.")


    # Make correlation plot for population
    corr_population_all = pearsonr(population_migration.total.tolist(), population_migration.net_out.tolist())
    fig, ax = plt.subplots(figsize=(8,6))
    color_dict_years = get_color_dict(population_migration, 'year')
    years = population_migration.year.drop_duplicates()
    for year in years:
        plt.scatter(population_migration.loc[population_migration.year == year].total, population_migration.loc[population_migration.year == year].net_out, color = color_dict_years[year])
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels([str(min(years)), str(max(years))])
    cb.ax.tick_params(size = 0)
    ax.text(0.5e7,-70000, 'Correlation: ' + "%0.3f" % corr_population_all[0])
    ax.text(0.5e7,-95000, 'p-value: ' + "%0.3f" % corr_population_all[1])
    ax.set_title('Total Population vs. Net Population Outflow', pad = 15)
    ax.set_xlabel('Total Population')
    ax.set_ylabel('Net Population Outflow')
    plt.tick_params(axis='both', which='major', length = 10, width = 2)
    st.pyplot(fig)

    st.markdown("""
    We calculated the correlation between the total population of a county and the net population outflow including all counties and all years. In Figure 3 we show that there is a moderate positive correlation (0.493) between total population and net population outflow. This is very reasonable given that intuitively we would expect counties with more people to lose more people and counties with fewer people to lose fewer people. Further, counties with high populations tend to be urban centers that have higher cost of living, as is addressed in further analysis.
    """)

  # Disasters EDA
  if choice == "Number of Disasters" or choice == "All Variables":
    st.markdown('''
          ### Number of Disasters

          At a very basic level, we want to understand the disasters that have occurred during the time period of population migration that we are studying, from 1993 until 2019. FEMA disaster data encompasses a wide array of disaster types, ranging from tornadoes to droughts. 
          ''')
    
    # Disasters Heat Map
    components.html("""
    <div id="observablehq-eb1119d4">
      <div class="observablehq-viewof-year_select"></div>
      <div class="observablehq-chart"></div>
      <div class="observablehq-update" style="display:none"></div>
    </div>
    <script type="module">
      import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
      import define from "https://api.observablehq.com/@ialsjbn/disasters.js?v=3";
      (new Runtime).module(define, name => {
        if (name === "viewof year_select") return Inspector.into("#observablehq-eb1119d4 .observablehq-viewof-year_select")();
        if (name === "chart") return Inspector.into("#observablehq-eb1119d4 .observablehq-chart")();
        if (name === "update") return Inspector.into("#observablehq-eb1119d4 .observablehq-update")();
      });
    </script>
    """, height = 600,)
    st.caption("Note: Click the play button to see where disasters are happening over time! You can also hover over a county to see more information.")

    # Number of Incidents by Disaster Type Bar Plot
    fig, ax = plt.subplots(figsize= (10,5))
    plt.bar(disaster_types.index, disaster_types.num_incidents, color = plt.get_cmap('viridis')(0.1), edgecolor = 'k')

    inc_types = disaster_types.incidentType
    ax.set_xticklabels(inc_types, rotation = 90)
    plt.xticks(np.linspace(0, max(disaster_types.index), num=max(disaster_types.index), endpoint=False))
    ax.set_xlim([-1,max(disaster_types.index)])

    ax.set_title('Number of Incidents by Disaster Type', pad = 15)
    ax.set_xlabel('Disaster Type')
    ax.set_ylabel('Number of Disasters')

    plt.tick_params(axis='both', which='major', length = 10, width = 2)

    st.pyplot(fig)

    st.markdown('''
    As a starting point, we want to understand what are some of the disasters that have been most prominent. In the figure above the total number of disasters that have occurred in the US between 1993-2019 are aggregated by type. Hurricanes and severe storms are by far the most common type of disaster, followed by floods and fires. As hurricanes and severe storms tend to affect coastal areas the most, we would expect disasters to drive migration into and out of these regions most significantly.
    ''')

    # Number of Disasters by Year Bar Plot
    disaster_highNet, disaster_lowNet = get_high_low_dfs(disaster_migration,highNet,lowNet)
    disaster_highNet_all = disaster_highNet.groupby(['year']).agg({'num_disasters':'sum'}).reset_index()
    disaster_lowNet_all = disaster_lowNet.groupby(['year']).agg({'num_disasters':'sum'}).reset_index()
    fig, ax = plt.subplots(figsize= (10,6))
    width = 0.4
    plt.bar(disaster_highNet_all.year - width/2, disaster_highNet_all.num_disasters, width, color = plt.get_cmap('viridis')(0.25), edgecolor = 'k')
    plt.bar(disaster_lowNet_all.year + width/2, disaster_lowNet_all.num_disasters, width, color = plt.get_cmap('viridis')(0.75), edgecolor = 'k')
    ax.set_title('Number of Disasters by Year', pad = 15)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Disasters')
    plt.tick_params(axis='both', which='major', length = 10, width = 2)
    plt.legend(['Highest Outflow','Highest Inflow'], loc='upper right', bbox_to_anchor=(0.42, 0.95),  frameon=False, fontsize = 18)
    st.pyplot(fig)

    st.markdown("""**Above: Total number of disasters, of all types, aggregated for the 20 counties with the highest net outflow and the 20 counties with the highest net inflow from 1993-2019** """)

    st.markdown(""" Aggregation of the total number of disasters of all types for the 20 counties with the highest net outflow and the 20 counties with the highest net inflow (lowest net outflow) reveals a counterintuitive trend. In Figure 5 we see that the counties with the highest net inflow of individuals actually have historically experienced more disasters per year than the counties with the highest net outflow. A potential explanation could be that housing prices decrease in areas that have experienced significant natural disasters which may serve as a counterweight to the risk incurred by living in an area prone to disasters.
    """)

    # Disaster Correlation Plot - Currently deleted
    # fig, ax = plt.subplots(figsize=(8,6))
    # corr_disasters_all = pearsonr(disaster_migration.num_disasters.tolist(), disaster_migration.net_out.tolist())
    # years = disaster_migration.year.drop_duplicates()
    # for year in years:
    #   plt.scatter(disaster_migration.loc[disaster_migration.year == year].num_disasters, disaster_migration.loc[disaster_migration.year == year].net_out, color = color_dict_years[year])

    # cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    # cb.set_ticks([0, 1])
    # cb.set_ticklabels([str(min(years)), str(max(years))])
    # cb.ax.tick_params(size = 0)

    # ax.text(3.5,170000, 'Correlation: ' + "%0.3f" % corr_disasters_all[0])
    # ax.text(3.5,150000, 'p-value: ' + "%0.3f" % corr_disasters_all[1])
    # #ax.text(1200,-60000, 'Correlation: ' + "%0.3f" % corr_disasters_all[0])
    # #ax.text(1200,-90000, 'p-value: ' + "%0.3f" % corr_disasters_all[1])

    # ax.set_title('Number of Disasters vs. Net Population Outflow', pad = 15)
    # ax.set_xlabel('Number of Disasters')
    # ax.set_ylabel('Net Population Outflow')
    # plt.tick_params(axis='both', which='major', length = 10, width = 2)

    # st.pyplot(fig)

  # Housing Price Index EDA
  if choice == "Housing Price Index" or choice == "All Variables":
    st.markdown('''
          ### Housing Price Index
          ''')
    # Housing Price Index Heat Map
    components.html("""
        <div id="observablehq-d9baf6ed">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/hpi.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-d9baf6ed .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-d9baf6ed .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-d9baf6ed .observablehq-update")();
          });
        </script>
        """, height = 600,)
    st.caption("Note: Click the play button to see how the HPI changes over time! You can also hover over a county to see more information.")
    
    # Data cleaning
    years = hpi_migration.year.drop_duplicates()
    hpi_highNet, hpi_lowNet = get_high_low_dfs(hpi_migration,highNet,lowNet)
    hpi_highNet_v0 = hpi_highNet.copy()
    hpi_highNet = hpi_highNet_v0.loc[hpi_highNet_v0.FIPS != 36061]
    color_dict_highNet = get_color_dict(hpi_highNet.loc[hpi_highNet.year == 2018].sort_values('net_out', ascending = True), 'FIPS')
    color_dict_lowNet = get_color_dict(hpi_lowNet.loc[hpi_lowNet.year == 2018].sort_values('net_out', ascending = False), 'FIPS')
    
    # Housing Price Index by Year Time Series Plots
    fig, ax = plt.subplots(1,2,figsize= (13,6), gridspec_kw={'width_ratios': [1, 1.25]})

    for FIPS in hpi_highNet.FIPS.drop_duplicates():
        ax[0].plot(hpi_highNet.loc[hpi_highNet.FIPS == FIPS].year, hpi_highNet.loc[hpi_highNet.FIPS == FIPS].hpi, color = color_dict_highNet[FIPS])

    for FIPS in hpi_lowNet.FIPS.drop_duplicates():
        ax[1].plot(hpi_lowNet.loc[hpi_lowNet.FIPS == FIPS].year, hpi_lowNet.loc[hpi_lowNet.FIPS == FIPS].hpi,  color = color_dict_lowNet[FIPS])

    fig.suptitle('Housing Price Index by Year', y = 1.01)
    ax[0].set_title('Highest Population Outflow', pad = 15)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('HPI')
    ax[1].set_title('Highest Population Inflow', pad = 15)
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('')

    ax[0].tick_params(axis='both', which='major', length = 10, width = 2)
    ax[1].tick_params(axis='both', which='major', length = 10, width = 2)

    # Color bar indicating most/least outflow/inflow
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels(['Least', 'Most'])
    cb.ax.tick_params(size = 0)

    st.write(fig)

    st.markdown(""" **Above: Housing Price Index by year for the 20 counties with the highest net outflow and highest net inflow, color coded by the magnitude of their net outflow or inflow, respectively**""")

    st.markdown("""
    In the figure above, the Housing Price Index is plotted by year for the 20 counties with the highest net outflow and inflow. The color of each line corresponds to the magnitude of the net outflow or inflow respectively.  Considering exclusively these counties we observe that the counties that experienced the largest outflow are in general the counties in which housing price indices have increased the most dramatically in the wake of the subprime mortgage crisis. Counties that experienced the largest inflow largely recovered from the subprime mortgage crisis but have not recovered prices beyond their pre-crisis level. For context, the three curves in the Highest Population Outflow plot that have the highest HPI levels in 2019 are all in the Bay Area. This concurs with anecdotal references to people leaving the Bay Area because of the excessive cost of living. Analysis of the effect of dramatically increasing income levels on both HPI and migration is warranted given these results. The two highest curves in the Lowest Population Outflow are also in California, but in rural California - specifically San Bernardino and Riverside counties. 
    """)

    # HPI vs Net Population Outflow Scatter Plot
    corr_hpi_all = pearsonr(hpi_migration.hpi.tolist(), hpi_migration.net_out.tolist())
    fig, ax = plt.subplots(figsize= (8,6))
    color_dict_years = get_color_dict(hpi_migration, 'year')

    for year in hpi_migration.year.drop_duplicates():
        plt.scatter(hpi_migration.loc[hpi_migration.year == year].hpi, hpi_migration.loc[hpi_migration.year == year].net_out, color = color_dict_years[year])

    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels([str(min(years)), str(max(years))])
    cb.ax.tick_params(size = 0)
    ax.text(1200,-60000, 'Correlation: ' + "%0.3f" % corr_hpi_all[0])
    ax.text(1200,-90000, 'p-value: ' + "%0.3f" % corr_hpi_all[1])

    ax.set_title('HPI vs. Net Population Outflow', pad = 15)
    ax.set_xlabel('HPI')
    ax.set_ylabel('Net Population Outflow')

    plt.tick_params(axis='both', which='major', length = 10, width = 2)
    st.pyplot(fig)

    st.markdown("""**Above: Housing price index by county and by year vs. net population outflow**""")

    st.markdown(""" The Housing Price Index dataset incorporating data from all counties in the US (excluding a few hundred rural counties with no data) indicates that there is a small positive correlation between increased housing price index and increased net population outflow, as plotted in Figure 7. This also agrees with anecdotal evidence indicating that there is a trend in people moving out of areas that are becoming more expensive.
    """)

  # Income EDA
  if choice == "Income" or choice == "All Variables":
    st.markdown('''
          ### Income
          ''')
    # Income Heat Map
    components.html("""
        <div id="observablehq-324b9012">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/income.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-324b9012 .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-324b9012 .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-324b9012 .observablehq-update")();
          });
        </script>
        """, height = 600,)
    st.caption("Note: Click the play button to see how the per capita income changes over time! You can also hover over a county to see more information.")

    # Per Capita Income By Year Time Series Plots 
    income_highNet, income_lowNet = get_high_low_dfs(income_migration,highNet,lowNet)
    color_dict_highNet = get_color_dict(income_highNet.loc[income_highNet.year == 2018].sort_values('net_out', ascending = True), 'FIPS')
    color_dict_lowNet = get_color_dict(income_lowNet.loc[income_lowNet.year == 2018].sort_values('net_out', ascending = False), 'FIPS')

    fig, ax = plt.subplots(1,2,figsize= (15,6), gridspec_kw={'width_ratios': [1, 1.25]})
    for FIPS in income_highNet.FIPS.drop_duplicates():
        ax[0].plot(income_highNet.loc[income_highNet.FIPS == FIPS].year, income_highNet.loc[income_highNet.FIPS == FIPS].per_capita_personal_income_dollars, color = color_dict_highNet[FIPS])

    for FIPS in income_lowNet.FIPS.drop_duplicates():
        ax[1].plot(income_lowNet.loc[income_lowNet.FIPS == FIPS].year, income_lowNet.loc[income_lowNet.FIPS == FIPS].per_capita_personal_income_dollars,  color = color_dict_lowNet[FIPS])
    fig.suptitle('Per Capita Income by Year', y = 1.01)
    ax[0].set_title('Highest Population Outflow', pad = 15)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Per Capita Income ($)')
    ax[1].set_title('Highest Population Inflow', pad = 15)
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('')
    ax[0].tick_params(axis='both', which='major', length = 10, width = 2)
    ax[1].tick_params(axis='both', which='major', length = 10, width = 2)

    # Color bar indicating most/least outflow/inflow
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels(['Least', 'Most'])
    cb.ax.tick_params(size = 0)
    st.pyplot(fig)

    st.markdown("""**Above: Per capita personal income by year for the 20 counties with the highest net outflow and highest net inflow, color coded by the magnitude of their net outflow or inflow, respectively**
    """)

    st.markdown("""
    In the figure above we plot the per capita income for the counties with the highest net outflow and inflow, again color coded by the magnitude of the outflow or inflow. In general, per capita income is significantly higher in counties with high net outflow than in counties with high net inflow. Interestingly, the county in each plot that has the highest outflow or inflow (indicated in yellow) appears roughly in the middle of each set of counties.
    """)

    # Per Capita Income vs Net Population Outflow Scatterplot
    corr_income_all = pearsonr(income_migration.per_capita_personal_income_dollars.tolist(), income_migration.net_out.tolist())
    years = income_migration.year.drop_duplicates()
    fig, ax = plt.subplots(figsize= (8,6))
    color_dict_years = get_color_dict(income_migration, 'year')

    for year in income_migration.year.drop_duplicates():
        plt.scatter(income_migration.loc[income_migration.year == year].per_capita_personal_income_dollars, income_migration.loc[income_migration.year == year].net_out, color = color_dict_years[year])
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels([str(min(years)), str(max(years))])
    cb.ax.tick_params(size = 0)
    ax.text(120000,150000, 'Correlation: ' + "%0.3f" % corr_income_all[0])
    ax.text(120000,120000, 'p-value: ' + "%0.3f" % corr_income_all[1])
    ax.set_title('Per Capita Income vs. Net Population Outflow', pad = 15)
    ax.set_xlabel('Per Capita Income ($)')
    ax.set_ylabel('Net Population Outflow')
    plt.tick_params(axis='both', which='major', length = 10, width = 2)
    st.pyplot(fig)

    st.markdown("""
    To further assess the relationship between the net population outflow and income, we computed the correlation between net outflow and per capita income and found that while there is a small net correlation between per capita income and net population outflow (0.38), it is not a particularly strong relationship. One factor that is not accounted for in our income dataset that could be very relevant is income inequality. For example, Teton, WY has the largest income per capita in the United States. However, the per capita income in Teton, WY is expected to be strongly bimodal, as this county has become a popular location for wealthy people to purchase large tracts of land, while the local population has income levels more in line with what would be expected for Wyoming. 
    """)

  # Employment EDA
  if choice == "Employment" or choice == "All Variables":
    st.markdown('''
          ### Employment
          ''')
    # Employment Heat Map
    components.html("""
        <div id="observablehq-7388290f">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/employment.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-7388290f .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-7388290f .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-7388290f .observablehq-update")();
          });
        </script>
        """, height = 600,)
    st.caption("Note: Click the play button to see how the employment numbers changes over time! You can also hover over a county to see more information.")

    # Employment Time Series Plots
    employment_highNet, employment_lowNet = get_high_low_dfs(employment_migration,highNet,lowNet)
    color_dict_highNet = get_color_dict(employment_highNet.loc[employment_highNet.year == 2018].sort_values('net_out', ascending = True), 'FIPS')
    color_dict_lowNet = get_color_dict(employment_lowNet.loc[employment_lowNet.year == 2018].sort_values('net_out', ascending = False), 'FIPS')

    fig, ax = plt.subplots(1,2,figsize= (15,6), gridspec_kw={'width_ratios': [1, 1.25]})

    for FIPS in employment_highNet.FIPS.drop_duplicates():
        ax[0].plot(employment_highNet.loc[employment_highNet.FIPS == FIPS].year, employment_highNet.loc[employment_highNet.FIPS == FIPS].employment, color = color_dict_highNet[FIPS])

    for FIPS in employment_lowNet.FIPS.drop_duplicates():
        ax[1].plot(employment_lowNet.loc[employment_lowNet.FIPS == FIPS].year, employment_lowNet.loc[employment_lowNet.FIPS == FIPS].employment,  color = color_dict_lowNet[FIPS])
    fig.suptitle('Total Jobs by Year', y = 1.01)
    ax[0].set_title('Highest Population Outflow', pad = 15)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Number of Jobs')
    ax[1].set_title('Highest Population Inflow', pad = 15)
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('')
    ax[0].tick_params(axis='both', which='major', length = 10, width = 2)
    ax[1].tick_params(axis='both', which='major', length = 10, width = 2)
    # Color bar indicating most/least outflow/inflow
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels(['Least', 'Most'])
    cb.ax.tick_params(size = 0)
    st.pyplot(fig)

    st.markdown("""**Above:
    Per capita personal income by year for the 20 counties with the highest net outflow and highest net inflow, color coded by the magnitude of their net outflow or inflow, respectively**
    """)
    st.markdown("""In the figure above we plot the total number of full time and part time jobs in each of the counties with the highest net inflow and outflow. In both cases, the counties with the highest total number of jobs have the highest population migration, whether out or in. 
    """)

    # Total Jobs vs Net Population Outflow Scatterplot
    corr_employment_all = pearsonr(employment_migration.employment.tolist(), employment_migration.net_out.tolist())
    years = employment_migration.year.drop_duplicates()
    fig, ax = plt.subplots(figsize= (8,6))
    color_dict_years = get_color_dict(employment_migration, 'year')
    for year in employment_migration.year.drop_duplicates():
        plt.scatter(employment_migration.loc[income_migration.year == year].employment, employment_migration.loc[employment_migration.year == year].net_out, color = color_dict_years[year])

    cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
    cb.set_ticks([0, 1])
    cb.set_ticklabels([str(min(years)), str(max(years))])
    cb.ax.tick_params(size = 0)
    ax.text(3.3e6,-70000, 'Correlation: ' + "%0.3f" % corr_employment_all[0])
    ax.text(3.3e6,-95000, 'p-value: ' + "%0.3f" % corr_employment_all[1])

    ax.set_title('Total Jobs vs. Net Population Outflow', pad = 15)
    ax.set_xlabel('Total Jobs')
    ax.set_ylabel('Net Population Outflow')

    plt.tick_params(axis='both', which='major', length = 10, width = 2)
    

    st.pyplot(fig)

    st.markdown("""**Above: Total number of jobs by county and by year vs. net population outflow**
    """)
    st.markdown("""In contrast to the housing price index and income data, the correlation between total number of jobs and net population outflow is relatively strong, 0.491, as we display in Figure 11. This could be related to counties with large numbers of jobs also being more densely populated and having higher cost of living. A combined analysis of job numbers, income, and housing prices could shed more light on this relationship and we pursue combinations of these factors further in our statistical modeling.
    """)

     
elif section =="Methodology":
  st.markdown("""
  # Methodology
  ## Time Series and Machine Learning Models
  In this project, we experimented with three different approaches to model the net population migration: a pure time-series ARIMA model, linear regression, and XGBoost. We used all three models to predict a **one-step forecast** of the net population migration (i.e. predict the value for the next year). 

  - **ARIMA**: ARIMA is a model that is commonly used for analyzing and forecasting time series data. This model only takes historical time series data as an input, to predict the future values. The ARIMA model has three parameters that include the number of lagged terms, the order of moving average, and the number of differencing required to make the time series stationary. This model is our baseline results. 
  - **Linear Regression**: Linear regression is a classic model used to predict continuous values. Using this model, we transformed our time series prediction problem into a regression problem by incorporating many other features that we hypothesize can help predict the values of the net migration better. The main assumption is that our predictors and the response variable have a linear relationship. 
  - **XGBoost**: Finally, we also experimented with the XGBoost model, a type of ensemble machine learning model. Because the algorithm leverages decision trees to make predictions, XGBoost is able to capture more non-linear relationships. 

  ## Feature Selection
  To determine the number of lagged values to include as a feature, we calculated the partial autocorrelation values for each county. Then, we took the lagged value that was most important across the counties. An example of the partial autocorrelation plot for a specific county (in this case Carroll County, MD)  is shown in the figure below. 
    """)

  fips = st.number_input(label='Enter FIPS Code',value=13237)
  # Need to center the plot
  col1,col2, col3 = st.columns([3,6,3])
  with col1:
    st.write("")
  with col2:
    # Make autocorrelation Plot
    series = county_net_out.loc[county_net_out['fips'] == fips, 'num_ind']
    # st.write(series)
    try:   
      fig = sm.graphics.tsa.plot_pacf(series.values.squeeze(),lags=10)
      temp = io.BytesIO()
      fig.savefig(temp,format="png")
      st.image(temp,width=400)  
    except:
      st.write('**Not enough data for this county**')
  with col3:
    st.write("")

  st.markdown('''
  From the autocorrelation plot above, we see that the first lagged value is the most important to predicting the net migration of a specific year. Though the 8th and 13th values also had larger values, we decided to not include those as we do not expect any seasonality occurring in our data. As a result, we only included the first lagged values in all our models. 

  In addition, we performed feature selection by leveraging p-values obtained from the results of linear regression. We first trained the linear regression using all six features and chose features that had a statistically significant p-value (around 0.05). These features are included in our final regression model. 

  For XGBoost, we performed a similar feature selection method as linear regression. However, because XGBoost can directly calculate feature importance, we selected features that had high feature importance in our final XGBoost model.

  ### Data Structure
  For the linear regression and XGBoost model, we transformed our problem into a supervised regression problem. The response variable is the net migration number at a given year. On the other hand, the features we incorporated were features with a one-year lag. For example, for the net migration value at 2010, we used feature values from 2009. An example of the data structure can be seen in the Figure below, where “num_ind” is our response variable. Note that the first row has NaN values because we don’t have information from the year 1992. This row is later dropped.    
  ''')

  data_struct_df = pd.read_csv('Datasets/all_features_dataframe.csv',index_col="Unnamed: 0")
  st.dataframe(data_struct_df)

  st.markdown('''
  ## Evaluation Metrics
  We used several evaluation metrics to evaluate our model. For feature selection, we used the p-values to determine whether or not to include the feature into our final model. For general model evaluation, we used **RMSE and R2 values**. These values are calculated for each year and each county. We also aggregated the error metrics to obtain an average score for the models. 

  ## Training and Validation Method
  Given the time series nature of our problem, we employed a walk-forward validation with expanding window technique for our training and validation method (Figure X). This was done using the following steps:

  1. We decided on test years between 2010-2019.

  2. We split the data into training and testing sets based on the test year, in which the training data consists of all data points before the test year, and the testing data consists of all data points of the test year. For example, if the test year is 2010, then the training data consisted of all points from the start of the dataset until 2009. 

  3. For a given test year, we trained our model using the training data.

  4. We predicted the value of our test year and calculated the error metrics. 

  5. Finally, we added the test year data into the training set such that the training set becomes larger. This is the expanding window technique. 

  6. Repeat steps 1-5 for each test year. 
  ''')

  st.image('Plots/walkforward.png', width = 500, caption = 'Illustrative example of walk-forward validation with an expanding window. (https://alphascientist.com/walk_forward_model_building.html)')
  st.markdown("""
  

  For the ARIMA model, this method was performed for each county (i.e. we trained 3051 counties x 10 years = 30510 models). However, for the linear regression and XGBoost models, we did not explicitly train a model separately for each county. Instead, we used the data points from all counties and trained it for a single model every year (i.e we trained only 10 models). 

  ## Projection Method
  We chose the best performing model to perform our projection predictions of the population migration in 2030. 

  In order to predict population migration in future years, we made approximate future projections of each of the input variables from 2020-2030. 

  Future values of total population were calculated using a linear fit to historic population values.  

  To project the total number of disasters per county per year into future years, we fit the aggregate number of disasters per county to a Poisson distribution. We calculated random samples of potential distributions of future disasters per year and averaged them over 100 samples in order to estimate the number of disasters per year but still provide a degree of variability per year.

  In order to project housing price index values into future years for incorporation into the model, we first converted the historic HPI values per county to a logarithmic scale. The subprime mortgage crisis of 2008 caused extreme levels of fluctuations in the HPI trends, but when plotted logarithmically the trend appears to be approximately linear for each county, with minor deviations due to the subprime mortgage crisis. We applied a linear fit to the logarithmic HPI values for each county. We then exponentiated this to generate future HPI values. We expected that more significant fluctuations will occur in housing markets in the next 30 years that are not accounted for in this fit, however based on the historic data it is likely that these crises will only cause temporary deviations from the overall exponential trend.

  We projected personal income per capita using an exponential fit for each county, which is reasonable due to the income data not being adjusted for inflation.

  To project total employment numbers (full-time plus part-time jobs) into future years for incorporation into the statistical model, we applied a linear fit to the historic number of jobs per county per year. 

  Our migration prediction models only predict a one-step forecast, thus the projections were obtained through a feedback loop. That is, we use our best model to predict the value for the next year, and use that predicted value as a feature to predict the next year. This loop is performed for every year from 2020 until 2030.  
  """)
elif section == "Results":
  st.markdown(""" # Results 
  ## Comparative Results
  Results for the RMSE and R$^2$ values of all three models we experimented with can be seen in Tables 1 and 2. 
  """)
  # components.html(
  #     """
  #     <div id="observablehq-a70836fb">
  #       <div class="observablehq-viewof-year_select"></div>
  #       <div class="observablehq-chart"></div>
  #       <div class="observablehq-update" style="display:none"></div>
  #     </div>
  #     <script type="module">
  #       import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
  #       import define from "https://api.observablehq.com/@ialsjbn/map_2019.js?v=3";
  #       (new Runtime).module(define, name => {
  #         if (name === "viewof year_select") return Inspector.into("#observablehq-a70836fb .observablehq-viewof-year_select")();
  #         if (name === "chart") return Inspector.into("#observablehq-a70836fb .observablehq-chart")();
  #         if (name === "update") return Inspector.into("#observablehq-a70836fb .observablehq-update")();
  #       });
  #     </script>
  #     """, height = 600,)
    st.markdown(""" 
  ## XGBoost Model Results """)

  results_table_1 = pd.DataFrame(index=["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","Average"])
  results_table_1['ARIMA'] = [1974.68,2194.96,1898.44,1625.18,1896.39,2677.59,1309.38,2002.05,833.01,734.07,1714.58]
  results_table_1['Linear Regression'] = [849.41,942.45,1260.88,967.98,1650.11,2478.72,1555.87,2231.31,1037.78,585.99,1356.05]
  results_table_1['XGBoost'] = [1142.07,1034.42,1249.18,1120.35,1796.54,1693.65,1429.09,2254.00,1678.95,864.00,1426.22]

  st.dataframe(results_table_1.style.format("{:.2f}"))

  st.markdown(""" 
  ### Linear Regression Model Results
  """)
  components.html(
          """
          <div id="observablehq-152f569d">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/linreg_diff.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-152f569d .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-152f569d .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-152f569d .observablehq-update")();
          });
        </script>
          """, height = 600,)
  st.markdown("""


  st.markdown(""" 
  ### XGBoost Model Results
  """)
  components.html(
          """
          <div id="observablehq-6397857c">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/xgboost_diff.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-6397857c .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-6397857c .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-6397857c .observablehq-update")();
          });
        </script>
          """, height = 600,)


  results_table_1 = pd.DataFrame(index=["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","Average"])
  results_table_1['ARIMA'] = [1974.68,2194.96,1898.44,1625.18,1896.39,2677.59,1309.38,2002.05,833.01,734.07,1714.58]
  results_table_1['Linear Regression'] = [849.41,942.45,1260.88,967.98,1650.11,2478.72,1555.87,2231.31,1037.78,585.99,1356.05]
  results_table_1['XGBoost'] = [1142.07,1034.42,1249.18,1120.35,1796.54,1693.65,1429.09,2254.00,1678.95,864.00,1426.22]

  st.dataframe(results_table_1.style.format("{:.2f}"))
  st.markdown("""**Above: RMSE results for the best models using three approaches**""")
  results_table_2 = pd.DataFrame(index=["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","Average"])
  results_table_2['ARIMA'] = [-0.285,-1.481,-0.297,0.405,0.519,-2.204,0.758,0.767,0.920,0.930,0.003]
  results_table_2['Linear Regression'] = [0.793,0.603,0.487,0.817,0.682,-1.384,0.704,0.740,0.890,0.961,0.529]
  results_table_2['XGBoost'] = [0.571,0.451,0.440,0.718,0.570,-0.278,0.712,0.706,0.676,0.904,0.547]
  
  st.dataframe(results_table_2.style.format("{:.2f}"))
  st.markdown("""**Above: R$^2$ results for the best models using three approaches**
  
  For ARIMA and linear regression, we noticed that the R2 was unusual for 2015-it was highly negative; however for XGBoost, there was not as much of a negative swing which suggests that the model was better at correcting for high fluctuations in migration that particular year.

  The ARIMA model, which is our baseline model, only uses historical net migration data per county to predict future values. We used parameters (1,0,0) for the ARIMA model. From Table 2, it can be seen that the R2 values of the ARIMA model are very close to 0. This might be caused by several factors:
  - The ARIMA model only has a very limited number of datapoints to train on. For each county, the ARIMA model only has 17 data points (one for each year from 1993-2010) to train from.
  - ARIMA model uses the whole time series data to predict future values. However, including values from 10 years ago, for example, may not be useful and may even cause the performance to degrade over time. 
  - Additional features are needed to predict future net migration values.  

  Given the poor performance on the ARIMA model, we experimented with the linear regression and XGBoost model. 

  The linear regression model incorporated additional variables to determine if there were other factors with explanatory power that impacted population migration. We trained and tested models with the following variables: population totals, number of disasters, per capita income, employment, and housing prices. With all variables, the linear regression model performed better than the ARIMA model; however, employment was not statistically significant (p > 0.05) for all projected years. On the other hand, the number of disasters was close to statistically significant (p ~ 0.05) for most of the test years.  We decided to keep the number of disasters but  removed employment and found that the R squared actually improved. We chose to drop employment from the final model of our linear regression model. 
  """)

  # Insert table with error results and coefficients from linear regression model here

  st.markdown("""
  One of the main assumptions of linear regression is that the relationship of interest is linear. In order to test for linearity, we plotted the expected values vs predicted values obtained from the linear regression model (Figure X) and found that the relationship is indeed linear. 
  """)
  st.markdown(""" 
  ## Projection Results
  """)
  components.html(
          """
        <div id="observablehq-756613fe">
          <div class="observablehq-viewof-year_select"></div>
          <div class="observablehq-chart"></div>
          <div class="observablehq-update" style="display:none"></div>
        </div>
        <script type="module">
          import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
          import define from "https://api.observablehq.com/@ialsjbn/popmig_proj.js?v=3";
          (new Runtime).module(define, name => {
            if (name === "viewof year_select") return Inspector.into("#observablehq-756613fe .observablehq-viewof-year_select")();
            if (name === "chart") return Inspector.into("#observablehq-756613fe .observablehq-chart")();
            if (name === "update") return Inspector.into("#observablehq-756613fe .observablehq-update")();
          });
        </script>
          """, height = 600,)
  
  st.markdown("""

  """)

  components.html(
        """
      <div id="observablehq-a40b4a45">
        <div class="observablehq-viewof-year_select"></div>
        <div class="observablehq-chart"></div>
        <div class="observablehq-update" style="display:none"></div>
      </div>
      <script type="module">
        import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
        import define from "https://api.observablehq.com/@ialsjbn/popmig_norm_proj.js?v=3";
        (new Runtime).module(define, name => {
          if (name === "viewof year_select") return Inspector.into("#observablehq-a40b4a45 .observablehq-viewof-year_select")();
          if (name === "chart") return Inspector.into("#observablehq-a40b4a45 .observablehq-chart")();
          if (name === "update") return Inspector.into("#observablehq-a40b4a45 .observablehq-update")();
        });
      </script>
        """, height = 600,)

  



elif section=="Conclusions & Limitations":
  st.markdown("""
  # Conclusions

  """)
  st.markdown("""
  ### Limitations
  The limitations of our study can be broadly separated into two categories: data limitations and methodology approaches. 

  #### Data Limitation
  In regards to our data, one main limitation of this approach is that it uses tax return data to calculate the net migration outflow for each county. Tax returns are usually only filed per household, so although the data approximates the number of individuals using the number of total exemptions, it may not be accurate. This also means that this data only tracks households/individuals who file taxes in the US.

  Another significant limitation of the approach is that it doesn’t account for international immigration into the counties. Therefore although counties might have negative net migration outflows every year, the total populations of the counties could still be growing, either due to births or immigration. 

  Additionally, our income and housing price index data is not adjusted for inflation, which over-values incomes in later years. If we had more time, we would incorporate an inflation adjustment in the dataset.

  Finally, if we had more time, we would try to include additional features that may better explain population migration, including climate related data such as temperature, drought, sea-level rise, etc. 

  #### Methodology Limitations
  As described earlier, our modeling choice involves a one-step forecast. Therefore, our population migration projection results in 2030 rely heavily on our predictions in every previous year. Instead of a one-step forecast, future work may involve building models for multi-step forecasts. However, we expect that the predictive power would significantly reduce. 

  Another modeling choice we made was that we focused on the net migration outflow. Future work can also focus on explicitly modeling the outflows and inflows of each origin-destination pair. 

  """)

elif section=="Supplemental Information":

  st.markdown(''' 
  ### AQI 
  We downloaded the AQI dataset from the United States Environmental Protection Agency (aqs.epa.gov). The AQI datasets are available by county by year, with a separate file for each year. All available datasets were downloaded and concatenated using pandas. This process was straightforward because all years had the same reported metrics. The data was then grouped by the five digit Federal Information Processing Standard (FIPS) code, which is a unique identifier for each county in the US. From this dataset, the median AQI was used to perform further analysis. Exploratory data analysis was performed on this dataset (below), but unfortunately too many counties were missing, so AQI was not included as a descriptor in the final model.
  ''')

  #### START AQI TIME PLOTS ####
  aqi_highNet, aqi_lowNet = get_high_low_10_dfs(aqi_migration,highNet,lowNet)
  fig, ax = plt.subplots(1,2,figsize= (15,6), gridspec_kw={'width_ratios': [1, 1.25]})

  color_dict_highNet = get_color_dict(aqi_highNet.loc[aqi_highNet.year == 2018].sort_values('net_out', ascending = True), 'FIPS')
  color_dict_lowNet = get_color_dict(aqi_lowNet.loc[aqi_lowNet.year == 2018].sort_values('net_out', ascending = False), 'FIPS')

  for FIPS in aqi_highNet.FIPS.drop_duplicates():
      ax[0].plot(aqi_highNet.loc[aqi_highNet.FIPS == FIPS].year, aqi_highNet.loc[aqi_highNet.FIPS == FIPS]['Median AQI'], color = color_dict_highNet[FIPS])

  for FIPS in aqi_lowNet.FIPS.drop_duplicates():
      ax[1].plot(aqi_lowNet.loc[aqi_lowNet.FIPS == FIPS].year, aqi_lowNet.loc[aqi_lowNet.FIPS == FIPS]['Median AQI'],  color = color_dict_lowNet[FIPS])

  fig.suptitle('Median AQI by Year', y = 1.01)
  ax[0].set_title('Highest Population Outflow', pad = 15)
  ax[0].set_xlabel('Year')
  ax[0].set_ylabel('Median AQI')
  ax[1].set_title('Highest Population Inflow', pad = 15)
  ax[1].set_xlabel('Year')
  ax[1].set_ylabel('')

  ax[0].tick_params(axis='both', which='major', length = 10, width = 2)
  ax[1].tick_params(axis='both', which='major', length = 10, width = 2)

  ax[0].set_xticks([1995,2000,2005,2010,2015])
  ax[1].set_xticks([1995,2000,2005,2010,2015])

  ax[0].set_xlim([min(aqi_highNet.year), max(aqi_highNet.year)])
  ax[1].set_xlim([min(aqi_lowNet.year), max(aqi_lowNet.year)])

  # Color bar indicating most/least outflow/inflow
  cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
  cb.set_ticks([0, 1])
  cb.set_ticklabels(['Least', 'Most'])
  cb.ax.tick_params(size = 0)

  st.pyplot(fig)

  #### END AQI TIME PLOTS ####

  st.markdown(''' Each line plotted in this graph represents an individual county. In general, the AQI appears to decrease over time, which is consistent with policy being enacted and technology being improved to reduce emissions. ''')

  # Make AQI Correlation Plot
  corr_aqi_all = pearsonr(aqi_migration['Median AQI'].tolist(), aqi_migration.net_out.tolist())
  fig, ax = plt.subplots(figsize= (8,6))
  color_dict_years = get_color_dict(migration_net, 'year')
  for year in migration_net.year.drop_duplicates():
      plt.scatter(aqi_migration.loc[aqi_migration.year == year]['Median AQI'], aqi_migration.loc[aqi_migration.year == year].net_out, color = color_dict_years[year])

  cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
  cb.set_ticks([0, 1])
  cb.set_ticklabels([str(min(aqi_migration.year)), str(max(aqi_migration.year))])
  cb.ax.tick_params(size = 0)
  ax.text(100,-75000, 'Correlation: ' + "%0.3f" % corr_aqi_all[0])
  ax.text(100,-100000, 'p-value: ' + "%0.3f" % corr_aqi_all[1])
  ax.set_title('Median AQI vs. Net Population Outflow', pad = 15)
  ax.set_xlabel('Median AQI')
  ax.set_ylabel('Net Population Outflow')
  plt.tick_params(axis='both', which='major', length = 10, width = 2)
  st.pyplot(fig)

  st.markdown('''
  This is an aggregate correlation plot of all the counties in the dataset. For each year available for each county, the AQI at that year vs the net migration outflow (total outflow from - total inflow to the county) is plotted as a datapoint. The colorbar shows the year that datapoint was taken at. There is a slight correlation in the direction we would expect, with higher AQIs (worse air quality) leading to higher migration outflows. However, this trend is not very strong.
  ''')

  #### AQI Heat Map ####
  # year = st.slider(label='Year',min_value = 1993, max_value = 2020)
  # aqi_map = aqis[aqis['year']==year]
  
  # fig = px.choropleth(aqi_map,geojson=counties, locations="FIPS",color='Median AQI',hover_name="County",color_continuous_scale="Viridis",range_color=(0,250),scope="usa",labels={'Median AQI':'Median AQI'})
  
  # st.write(fig)

  st.markdown("""
  ### FMR
  We downloaded Fair Market Rent (FMR) data from the Department of Housing and Urban Development (HUD) website via their Office of Policy Development and Research (PD&R). This dataset includes the 40th percentile rental rates by county and by year for Studio, 1, 2, 3, and 4 Bedroom units from 2004-2021. 
  """)
  # FMR Scatter Plot
  corr_fmr_0 = pearsonr(fmr_migration.fmr_0.tolist(), fmr_migration.net_out.tolist())
  corr_fmr_1 = pearsonr(fmr_migration.fmr_1.tolist(), fmr_migration.net_out.tolist())
  corr_fmr_2 = pearsonr(fmr_migration.fmr_2.tolist(), fmr_migration.net_out.tolist())
  corr_fmr_3 = pearsonr(fmr_migration.fmr_3.tolist(), fmr_migration.net_out.tolist())
  corr_fmr_4 = pearsonr(fmr_migration.fmr_4.tolist(), fmr_migration.net_out.tolist())
  fig, ax = plt.subplots(2,3, figsize = (28,18))

  color_dict = get_color_dict(fmr_migration, 'year')

  for year in fmr_migration.year.drop_duplicates():
      ax[0,0].scatter(fmr_migration.loc[fmr_migration.year == year].fmr_0, fmr_migration.loc[fmr_migration.year == year].net_out, color = color_dict[year])

  for year in fmr_migration.year.drop_duplicates():
      ax[0,1].scatter(fmr_migration.loc[fmr_migration.year == year].fmr_1, fmr_migration.loc[fmr_migration.year == year].net_out, color = color_dict[year])

  for year in fmr_migration.year.drop_duplicates():
      ax[0,2].scatter(fmr_migration.loc[fmr_migration.year == year].fmr_2, fmr_migration.loc[fmr_migration.year == year].net_out, color = color_dict[year])

  for year in fmr_migration.year.drop_duplicates():
      ax[1,0].scatter(fmr_migration.loc[fmr_migration.year == year].fmr_3, fmr_migration.loc[fmr_migration.year == year].net_out, color = color_dict[year])

  for year in fmr_migration.year.drop_duplicates():
      ax[1,1].scatter(fmr_migration.loc[fmr_migration.year == year].fmr_4, fmr_migration.loc[fmr_migration.year == year].net_out, color = color_dict[year])

  ax[1,0].set_position([0.24,0.125, 0.228, 0.343])
  ax[1,1].set_position([0.55,0.125, 0.228, 0.343])
  ax[1,2].set_visible(False)
      
  fig.suptitle('Fair Market Rent vs. Net Outflow', fontsize =  25)

  ax[0,0].set_title('Studio', pad = 15)
  #ax[0,0].set_xlabel('FMR', fontsize=30, labelpad = 15)
  ax[0,0].set_ylabel('Net Outflow', labelpad = 15)
  ax[0,0].tick_params(axis='both', which='major', width = 2, length = 10)

  ax[0,1].set_title('1 Bedroom', pad = 15)
  #ax[0,1].set_xlabel('FMR', labelpad = 15)
  #ax[0,1].set_ylabel('Net Outflow', labelpad = 15)
  ax[0,1].tick_params(axis='both', which='major', width = 2, length = 10)

  ax[0,2].set_title('2 Bedroom', pad = 15)
  #ax[0,2].set_xlabel('FMR', labelpad = 15)
  #ax[0,2].set_ylabel('Net Outflow', labelpad = 15)
  ax[0,2].tick_params(axis='both', which='major', width = 2, length = 10)

  ax[1,0].set_title('3 Bedroom', pad = 15)
  ax[1,0].set_xlabel('FMR', labelpad = 15)
  ax[1,0].set_ylabel('Net Outflow', labelpad = 15)
  ax[1,0].tick_params(axis='both', which='major', width = 2, length = 10)

  ax[1,1].set_title('4 Bedroom', pad = 15)
  ax[1,1].set_xlabel('FMR', labelpad = 15)
  #ax[1,1].set_ylabel('Net Outflow', fontweight = 'bold', labelpad = 15)
  ax[1,1].tick_params(axis='both', which='major', width = 2, length = 10)

  #ax[0,0].tick_params(axis='both', which='major', labelsize=20)
  
  ax[0,0].text(1200,-70000, 'Correlation: ' + "%0.3f" % corr_fmr_0[0])
  ax[0,0].text(1200,-90000, 'p-value: ' + "%0.3f" % corr_fmr_0[1])

  ax[0,1].text(1500,-70000, 'Correlation: ' + "%0.3f" % corr_fmr_1[0])
  ax[0,1].text(1500,-90000, 'p-value: ' + "%0.3f" % corr_fmr_1[1])

  ax[0,2].text(1800,-70000, 'Correlation: ' + "%0.3f" % corr_fmr_2[0])
  ax[0,2].text(1800,-90000, 'p-value: ' + "%0.3f" % corr_fmr_2[1])

  ax[1,0].text(2200,-70000, 'Correlation: ' + "%0.3f" % corr_fmr_3[0])
  ax[1,0].text(2200,-90000, 'p-value: ' + "%0.3f" % corr_fmr_3[1])

  ax[1,1].text(2600,-70000, 'Correlation: ' + "%0.3f" % corr_fmr_4[0])
  ax[1,1].text(2600,-90000, 'p-value: ' + "%0.3f" % corr_fmr_4[1])
      
  cb = plt.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(0,1), cmap='viridis'))
  cb.set_ticks([0, 1])
  cb.set_ticklabels([str(min(fmr_migration.year)), str(max(fmr_migration.year))])
  cb.ax.tick_params(size = 0)

  st.pyplot(fig)

  st.markdown("""
  FMR rates did actually indicate a small positive correlation between rental rates and net migration outflow, between 0.14 and 0.18 depending on the size of the unit. This is comparable to the correlation between Housing Price Index and net outflow (0.117) shown in Figure 7. However, the FMR data only dates back to 2004 making it a less desirable feature to include in our analysis. We decided to neglect FMR in our model as the reasons for the positive correlation are most likely the same as the reasons for the positive correlation seen in the HPI data, namely cost of living, which is already incorporated in our model.
  """)
