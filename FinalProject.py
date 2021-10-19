import streamlit as st
# from streamlit_observable import observable
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

  all_aqi_data = pd.read_csv('Datasets/all_aqi_migration_data.csv')
  county_net_out = pd.read_csv('Datasets/county_net_out.csv')

  hpis = pd.read_csv('Datasets/HPI.csv')
  hpis['FIPS'] = ["%05d" % elem for elem in hpis['FIPS']]

  return lowFIPS,highFIPS,popmig,aqis,all_aqi_data,county_net_out,hpis

lowFIPS,highFIPS,popmig,aqis,all_aqi_data,county_net_out,hpis = import_data()


##### END DATA IMPORTING SECTION #####

#### TITE AND HEADER ####
# Title and header
st.markdown(''' # Landscape of the New America: How the US population will be redistributed in 2050 ''')
st.markdown(''' ## Team 24 ''')
st.markdown('''Danah Park | Devi Ganapathi | Emily Wang | Gabrielle Cardoza | Irene Alisjahbana | Liz Peterson | Noemi Valdez ''')

section = st.sidebar.selectbox("Outline",("Executive Summary","Project Description","Datasets","Exploratory Data Analysis","Model Building","Results","Conclusions","Supplemental Information"))

if section == "Project Description":
    st.markdown(''' 
    ## Project Description
    
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

elif section == "Datasets":

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
    
elif section == "Exploratory Data Analysis":
    
  st.markdown('''
  ### Visualizing Trends for Counties
  To visualize the trends in the data over time, we chose two subsets of counties to look at. The first subset is the group of counties with the highest net outflows in population, as observed in 2018 (to avoid COVID-19 related effects). The second subset is the group of counties with the lowest net outflows in population (highest net inflows), also as observed in 2018. 
  ''')

  # ### HPI Heat Map
  # year = st.slider(label='Year',min_value = 1993, max_value = 2020)
  # hpi_map = hpis[hpis['year']==year]
  
  # fig = px.choropleth(hpi_map,geojson=counties, locations="FIPS",color='hpi',color_continuous_scale="Viridis",scope="usa",labels={'hpi':'HPI'})
  
  # st.write(fig)

  # Notes from Chris: Drop EDA into the appendix (change section name)
  # Features are not that interesting
  # Do EDA on response variable
  # Journalistic style writing - most important first
  # Add Executive summary section at the beginning
  # Make consistent first person
  # Executive summary: Scope and results? Main findings - abstract, error, factors that had an effect, no more than ~250 words 

  st.markdown('''
        ### Population Migration
        ''')
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

  st.markdown('''
        ### Population
        ''')

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

  st.markdown('''
        ### Income
        ''')

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

  st.markdown('''
        ### Employment
        ''')

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

  st.markdown('''
        ### Housing Price Index
        ''')

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

  st.markdown('''
        ### Number of Disasters
        ''')

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



     
elif section =="Model Building":
  st.markdown("""
  ## Methodology
  ### Time Series and Machine Learning Models
  In this project, we experimented with three different approaches to model the net population migration: a pure time-series ARIMA model, linear regression, and XGBoost. We used all three models to predict a **one-step forecast** of the net population migration (i.e. predict the value for the next year). 

  - **ARIMA**: ARIMA is a model that is commonly used for analyzing and forecasting time series data. This model only takes historical time series data as an input, to predict the future values. The ARIMA model has three parameters that include the number of lagged terms, the order of moving average, and the number of differencing required to make the time series stationary. This model is our baseline results. 
  - **Linear Regression**: Linear regression is a classic model used to predict continuous values. Using this model, we transformed our time series prediction problem into a regression problem by incorporating many other features that we hypothesize can help predict the values of the net migration better. The main assumption is that our predictors and the response variable have a linear relationship. 
  - **XGBoost**: Finally, we also experimented with the XGBoost model, a type of ensemble machine learning model. Because the algorithm leverages decision trees to make predictions, XGBoost is able to capture more non-linear relationships. 

  ### Feature Selection
  To determine the number of lagged values to include as a feature, we calculated the partial autocorrelation values for each county. Then, we took the lagged value that was most important across the counties. An example of the partial autocorrelation plot for a specific county (in this case Carroll County, MD)  is shown in the figure below. 
    """)

  # Make autocorrelation Plot
  fips = st.number_input(label='Enter FIPS Code',value=13237)
  series = county_net_out.loc[county_net_out['fips'] == fips, 'num_ind']
  # st.write(series)
  try:
    fig = sm.graphics.tsa.plot_pacf(series.values.squeeze(),lags=10)
    st.pyplot(fig)  
  except:
    st.write('**Not enough data for this county**')

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
  ### Evaluation Metrics
  We used several evaluation metrics to evaluate our model. For feature selection, we used the p-values to determine whether or not to include the feature into our final model. For general model evaluation, we used **RMSE and R2 values**. These values are calculated for each year and each county. We also aggregated the error metrics to obtain an average score for the models. 

  ### Training and Validation Method
  Given the time series nature of our problem, we employed a walk-forward validation with expanding window technique for our training and validation method (Figure X). This was done using the following steps:

  1. We decided on test years between 2010-2019.

  2. We split the data into training and testing sets based on the test year, in which the training data consists of all data points before the test year, and the testing data consists of all data points of the test year. For example, if the test year is 2010, then the training data consisted of all points from the start of the dataset until 2009. 

  3. For a given test year, we trained our model using the training data.

  4. We predicted the value of our test year and calculated the error metrics. 

  5. Finally, we added the test year data into the training set such that the training set becomes larger. This is the expanding window technique. 

  6. Repeat steps 1-5 for each test year. 
  ''')

  st.image('Plots/walkforward.png')
  st.markdown("""
  Illustrative example of walk-forward validation with an expanding window. [Source](https://alphascientist.com/walk_forward_model_building.html)

  For the ARIMA model, this method was performed for each county (i.e. we trained 3051 counties x 10 years = 30510 models). However, for the linear regression and XGBoost models, we did not explicitly train a model separately for each county. Instead, we used the data points from all counties and trained it for a single model every year (i.e we trained only 10 models). 

  ### Projection Method
  We chose the best performing model to perform our projection predictions of the population migration in 2030. Because our model only predicts a one-step forecast, the projections were obtained through a feedback loop. That is, we use our best model to predict the value for the next year, and use that predicted value as a feature to predict the next year. This loop is performed for every year from 2020 until 2030. 
  """)
elif section == "Results":

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

elif section=="Supplemental Information":
  
  st.markdown(''' 
  ### AQI 
  We downloaded the AQI dataset from the United States Environmental Protection Agency (aqs.epa.gov). The AQI datasets are available by county by year, with a separate file for each year. All available datasets were downloaded and concatenated using pandas. This process was straightforward because all years had the same reported metrics. The data was then grouped by the five digit Federal Information Processing Standard (FIPS) code, which is a unique identifier for each county in the US. From this dataset, the median AQI was used to perform further analysis. Exploratory data analysis was performed on this dataset (below), but unfortunately too many counties were missing, so AQI was not included as a descriptor in the final model.
  ''')

  #### START AQI TIME PLOTS ####
  # Counties with lowest net migration outflow
  start_year,end_year = st.select_slider(label='Year Range to Plot',options=np.arange(1993,2020,1),value=(1993,2019))
  colors = cm.viridis(np.linspace(0,1,len(lowFIPS)))
  fig,ax = plt.subplots(figsize=(10,6))
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
  # start_year,end_year = st.select_slider(label='Year Range to Plot',options=np.arange(1993,2020,1),value=(1993,2019))
  colors = cm.viridis(np.linspace(0,1,len(lowFIPS)))
  fig,ax = plt.subplots(figsize=(10,6))
  i = 0
  for fips in highFIPS:
    x = aqis[aqis['FIPS']==fips]
    x = x[x['year'].isin(np.arange(start_year,end_year,1))]['year']
    y = aqis[aqis['FIPS']==fips]
    y = y[y['year'].isin(np.arange(start_year,end_year,1))]['Median AQI']
    plt.plot(x,y,color=colors[i])
    i += 1
  plt.xlabel('Year')
  plt.ylabel('Median AQI')
  plt.title('Counties with Highest Net Outflows')
  
  st.pyplot(fig)

  #### END AQI TIME PLOTS ####

  st.markdown(''' Each line plotted in this graph represents an individual county. In general, the AQI appears to decrease over time, which is consistent with policy being enacted and technology being improved to reduce emissions. ''')

  # Make AQI Correlation Plot
  corr = pearsonr(all_aqi_data['AQI'],all_aqi_data['Net Migration Outflow'])
  fig,ax = plt.subplots(1,1,figsize=(7,6))
  plt.scatter(all_aqi_data['AQI'],all_aqi_data['Net Migration Outflow'],c=all_aqi_data['year'])  
  plt.xlabel('Median AQI')
  plt.ylabel('Net Migration Outflow')
  plt.colorbar()
  # Customize where the annotation appears by changing the scaling values below

  plt.text(x=0.37*np.max(all_aqi_data['AQI']),y=np.min(all_aqi_data['Net Migration Outflow'])-0*(np.max(all_aqi_data['Net Migration Outflow'])-np.min(all_aqi_data['Net Migration Outflow'])),s='Correlation: ' + "%0.3f" % corr[0])

  plt.text(x=0.5*np.max(all_aqi_data['AQI']),y=np.min(all_aqi_data['Net Migration Outflow'])+0.1*(np.max(all_aqi_data['Net Migration Outflow'])-np.min(all_aqi_data['Net Migration Outflow'])),s='p-value: ' + "%0.3f" % corr[1])

  st.pyplot(fig)
  st.markdown('''
  This is an aggregate correlation plot of all the counties in the dataset. For each year available for each county, the AQI at that year vs the net migration outflow (total outflow from - total inflow to the county) is plotted as a datapoint. The colorbar shows the year that datapoint was taken at. There is a slight correlation in the direction we would expect, with higher AQIs (worse air quality) leading to higher migration outflows. However, this trend is not very strong.
  ''')

  #### AQI Heat Map ####
  year = st.slider(label='Year',min_value = 1993, max_value = 2020)
  aqi_map = aqis[aqis['year']==year]
  
  fig = px.choropleth(aqi_map,geojson=counties, locations="FIPS",color='Median AQI',hover_name="County",color_continuous_scale="Viridis",range_color=(0,250),scope="usa",labels={'Median AQI':'Median AQI'})
  
  st.write(fig)


