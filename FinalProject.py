import streamlit as st
from streamlit_observable import observable
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
plt.style.use('../EDA/mplstyles/DGplots.mplstyle')

##### DATA IMPORTING SECTION #####
# Import all relevant datasets in this section so they'll be accessible in all sections
lowNet = pd.read_csv('../Datasets/Cleaned Data/smallestNetOutflows.csv')
highNet = pd.read_csv('../Datasets/Cleaned Data/largestNetOutflows.csv')
lowNet = lowNet.rename(columns={'Unnamed: 0':'FIPS'})
highNet = highNet.rename(columns={'Unnamed: 0':'FIPS'})
lowNet['FIPS'] = ["%05d" % elem for elem in lowNet['FIPS']]
highNet['FIPS'] = ["%05d" % elem for elem in highNet['FIPS']]
popmig = pd.read_csv('../Datasets/Cleaned Data/population_migration.csv')
popmig['FIPS'] = ["%05d" % elem for elem in popmig['FIPS']]
popmig['dest_FIPS'] = ["%05d" % elem for elem in popmig['dest_FIPS']]
aqis = pd.read_csv('../Datasets/Cleaned Data/AQI_by_County.csv')
aqis['FIPS'] = ["%05d" % elem for elem in aqis['FIPS']]
lowFIPS = lowNet['FIPS'].to_list()
highFIPS = highNet['FIPS'].to_list()

##### END DATA IMPORTING SECTION #####

#### TITE AND HEADER ####
# Title and header
st.markdown(''' # Landscape of the New America: How the US population will be redistributed in 2050 ''')
st.markdown(''' ## Team 24 ''')
st.markdown('''Danah Park | Devi Ganapathi | Emily Wang | Gabrielle Cardoza | Irene Alisjahbana | Liz Peterson | Noemi Valdez ''')

section = st.sidebar.selectbox("Outline",("Project Description","Exploratory Data Analysis",
"Model Building","Results","Conclusions"))

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
    
    ## Data Analysis & Computation

    ''')

    st.markdown(' ### AQI ')
    
elif section == "Exploratory Data Analysis":
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
    
    # year = st.slider(label="Year", min_value=1993,max_value=2020,value=2019)
    # with st.echo():
    observers = observable("Year",notebook="@ialsjbn/map_2019",targets=["year_select","chart"],observe=["year_select"])
    # year_select = observers.get("year_select")
    # observable("Selected Year Projection",notebook="@ialsjbn/map_2019",targets=["chart"],redefine={"year_select":year})
    # with st.echo():
    #     observers_a = observable("Matrix Input A", 
    #         notebook="d/9e0aa2504039dbcd",
    #         targets=["viewof a"],
    #         observe=["a"]
    #     )
    #     observers_b = observable("Matrix Input B", 
    #         notebook="d/9e0aa2504039dbcd",
    #         targets=["viewof b"],
    #         observe=["b"]
    #     )
    #     if bool(observers_a) and bool(observers_b):
    #         with st.echo():
    #             a = observers_a.get("a")
    #             b = observers_b.get("b")

    #     # if explain:
    #     #     st.write("Then let's multiply these two matricies together:")

    #     with st.echo():
    #         result = np.matmul(a, b)

    #     # if explain:
    #     #     st.write("""Finally, let's use that `"prettyExample"` cell
    #     #         to render the multiplication result out!""")

    #     with st.echo():
    #         observable("np.matmul result", 
    #             notebook="d/9e0aa2504039dbcd",
    #             targets=["prettyExample"],
    #             redefine={
    #                 "example": result.tolist()
    #             }
    #         )
 