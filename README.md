
# Project Abstract

Due to climate change and the disruption of ecosystems worldwide, wildfires are increasingly impacting environment, infrastructure, and human lives globally. Additionally, an exacerbating climate crisis means that these losses would continue to grow if preventative measures are not implemented. Though recent advancements in artificial intelligence enable wildfire management techniques, most deployed solutions focus on detecting wildfires after ignition. The development of predictive techniques with high accuracy requires extensive datasets to train machine learning models. This paper presents the California Wildfire Inventory (CAWFI), a wildfire database of over 34 million data points for building and training wildfire prediction solutions, thereby potentially preventing megafires and flash fires by addressing them before they spark. The dataset compiles daily historical California wildfire data from 2012 to 2018 and indicator data from 2012 to 2022. The indicator data consists of leading indicators (meteorological data correlating to wildfire-prone conditions), trailing indicators (environmental data correlating to prior and early wildfire activity), and geological indicators (vegetation and elevation data dictating wildfire risk and spread patterns).

## Directory Structure

The directory structure below outlines the main components of the project:

```
Original Data/
    ├── daily_co/                # CO (Carbon Monoxide) data collected daily
    ├── daily_dewpoint/          # Daily dewpoint measurements
    ├── daily_no2/               # Nitrogen Dioxide (NO2) levels recorded daily
    ├── daily_pm10/              # Daily PM10 particulate matter data
    ├── daily_pm25/              # Daily PM2.5 particulate matter data
    ├── daily_TEMP/              # Daily temperature data
    ├── daily_wildfire/          # Wildfire-related data collected daily
    └── daily_wind/              # Daily wind speed and direction data

   sql_data/
      ├── daily_co.sql           # SQL file containing CO data for daily measurements
      ├── daily_no.sql           # SQL file for NO2 (Nitrogen Dioxide) data
      ├── daily_pm10.sql         # SQL data for PM10 particulate matter measurements
      ├── daily_pm25.sql         # SQL data for PM2.5 particulate matter measurements
      ├── daily_temp.sql         # SQL data for temperature records
      ├── daily_wildfire.sql     # SQL data containing wildfire-related information
      └── daily_wind.sql         # SQL data for wind-related measurements

   instructions.md               # Instructions document on how to use the dataset and process it
   geological_indicators.md      # Geological indicators that help in understanding the dataset context
   metadata.xml                  # Metadata file containing key information about the dataset
   wildfire_data.csv             # CSV format file containing wildfire data
   ndvi.png                      # Image of the NDVI (Normalized Difference Vegetation Index) visual
   elevation.png                 # Elevation map image for geographic reference

Processing Files/
    ├── met_env_heatmap.py     # Interpolate and generate heatmaps from meteorological/environmental data
    ├── parse_met_env.py       # Parse the meteorological/environmental metadata and preprocess data
    ├── process_geo.py         # Process and analyze geospatial data
    └── wildfire_heatmap.py    # Interpolate and generate wildfire heatmaps from wildfire data

elevation.png                 # Elevation geospatial data
ndvi.png                      # NDVI (Normalized Difference Vegetation Index) geospatial data
geological_indicators.md      # Geological indicators processing instructions
metadata.xml                  # Metadata file containing key information about the dataset
```

## Contact

Rohan Tan Bhowmik (rbhowmik@stanford.edu)