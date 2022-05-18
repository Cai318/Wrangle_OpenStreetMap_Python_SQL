# Wrangle_OpenStreetMap_Python_SQL 
## By Callie Lamb

## Introduction

>This project was completed to satisfy the requirements for Udacity’s “Data Wrangling” course in the Data Analysis NanoDegree program. The data used in this analysis is an export from OpenStreetMap.org via Overpass API, which is a mirror of OpenStreetMap’s extensive database. I chose Yellowstone National Park because it is one of my favorite places to visit.
>
>This document provides a breif overview of each of the files in this project, and a detailed explanation of how I used python to parse through the XML data, audit, and programmatically clean the data before being written to CSVs and an SQL database. Then query the database through SQL statements written in python to retrieve various information.

## Overview of Project Files 

### Yellowstone.osm	
>Main osm XML file that is used for the project. Contains map information in the form of “nodes” (geographic position), “ways” (connection routes), “relations” (relationships between nodes and ways), and “tags” (metadata attached to nodes, ways, or a relation). More information about this file type can be found here: https://docs.fileformat.com/gis/osm/.

### create_sample.py
>Creates a Sample.osm from Yellowstone.osm that is about 1/10th it’s size. I use this to validate my code, as it runs much faster. 

### main.py
>Where the main function is. At the top of this file is where I apoint which osm file to use.

### audit.py
>When specific element types run through these functions as it is parsing through the osm XML in the main function, certain criteria are checked and fixed before it returns to the main function.

### schema.py
>Contains the format for each SQL table that will be made. 

### create_db.py
>Creates the SQL database named “Yellowstone_SQL_DB.db”.

### queries.py
>Contains SQL queries, written through python. 

### nodes.csv, nodes_tags.csv, ways.csv, ways_nodes.csv, and ways_tags.csv
>These are from running main.py where the data is cleaned before being written to these CSVs.

### Yellowstone_SQL_DB.db
>This is the SQL database that is created from running create_db.py

### map_link
>Contains the link for the map data export and information about the map.

### Rubric_Answers.pdf
>My responses to the rubric questions from Udacity.
