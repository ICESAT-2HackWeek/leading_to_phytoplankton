# Leading to Phytoplankton Final Project

06/18/2020
ICESat-2 Hackweek

# Team Members

#Nicole Abib  
#Kelsey Bisson   
#Alessandro Di Bella   
#Ted Maksym     
#Romina Piunno     

#Rachel Tilling      

#Molly Wieringa       



Thanks to Lindsey Heagey and Joachim Meyer for the template, provided originally for [Geohackweek](https://github.com/geohackweek/sample_project_repository).

### Goals

Hackweek Goal: Query, Download, and Visualize coincident ICESat-2, Sentinel-2, and Argo Float data.     



Long term goal: Create a package that will download data of interest for a specified time period and bounding box to study changing ice-ocean interactions & properties. This package will be modular so that other data products can easily be incorporated. 

Specific goals: 
1. Create a tool for identifying (near) co-indicdent measurements across varied datasets(specifically with Argo float data, MODIS and/or Sentinel imagery, and ICESat-2 tracks)

2. Formulate scripts to develop or isolate parameters from ATL03 data that might be relevant to larger science questions for which the above measurements are relevant

3. Become Python gods. 

### other notes

We would like to have 2 Notebooks as deliverables and a clear use-case story. We hope to develop some pretext for a potential GUI by incorporating widgets into the co-incident measurements tool. 

## Folders

### `contributors`
Each team member has it's own folder under contributors, where he/she can
work on their contribution. Having a dedicated folder for one-self helps to 
prevent conflicts when merging with master.

### `notebooks`

The project presentation is 'presentation.ipynb'
Other visualization notebooks and sanboxes for scrap work are included.

### `scripts`
These include download scripts for ICESat-2, sentinel -2, MODIS, VIIRS, SeaWiFS. Argo download scripts are not included because at this time it is not possible to search an API for synthetic biogeochemical floats around a bounding box and time. Future development will include these tools and others. Colocated data scripts are included as well as basic scripts to interpret ATL03 and ATL07 attributes.

