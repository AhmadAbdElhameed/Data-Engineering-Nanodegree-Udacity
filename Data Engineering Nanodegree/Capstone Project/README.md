# Analysis of Immigration to the United States
### Data Engineering Capstone Project

#### Project Summary

This project aims to be able to answers questions on US immigration such as what are the most popular cities for immigration, what is the gender distribution of the immigrants, what is the visa type distribution of the immigrants, what is the average age per immigrant and what is the average temperature per month per city. We extract data from 3 different sources, the I94 immigration dataset of 2016, city temperature data from Kaggle and US city demographic data from OpenSoft. We design 4 dimension tables: Cities, immigrants, monthly average city temperature and time, and 1 fact table: Immigration. We use Spark for ETL jobs and store the results in parquet for downstream analysis.

To accomplish this study, we will be using the following datasets:

* **I94 Immigration Data**: This data comes from the US National Tourism and Trade Office and includes the contents of the i94 form on entry to the united states. A data dictionary is included in the workspace.
The dataset can be found [here.]https://www.trade.gov/national-travel-and-tourism-office

* **World Temperature Data**: This dataset comes from Kaggle and includes the temperatures of various cities in the world fomr 1743 to 2013.
  The dataset can be found [here.](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
* **U.S. City Demographic Data**: This data comes from OpenSoft. It contains information about the demographics of all US cities and census-designated places with a population greater or equal to 65,000 and comes from the US Census Bureau's 2015 American Community Survey.
  The dataset can be found [here.](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/)
* **Airport Code Table**: This is a simple table of airport codes and corresponding cities.
  The dataset can be found [here.](https://datahub.io/core/airport-codes#data)

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

