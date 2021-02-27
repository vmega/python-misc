#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Downlading data from energy-charts.de and feeding them in your sql table
"""
from datetime import datetime
import urllib2
import json
import pandas as pd
from sqlalchemy import create_engine
from passwords import host, user, passw, port, database

cnx = create_engine('mysql+pymysql://' + user + ':' + passw + '@' +
                    host + ':' + str(port) + '/' + database, echo=False)

powerTypeDict = {
    "Hydro Power": "hydro",
    "Biomass": "biomass",
    "Uranium": "nuclear",
    "Brown Coal": "lignite",
    "Hard Coal": "hardCoal",
    "Oil": "oil",
    "Gas": "gas",
    "Wind": "wind",
    "Solar": "pvSolar",
    "Others": "other",
    "Load": "electricalLoad"}

year = 2016
dataframe_generation = pd.DataFrame([])

while year <= datetime.now().year:
    data = json.load(urllib2.urlopen('https://www.energy-charts.de/energy/month_%s.json' % year))
    for dict in data:
        originalFueltype = dict["key"][0]["en"]  # dictionary in a 1-element list in a dictionary {[{}]}
        newFueltype = powerTypeDict[originalFueltype]
        for entry in dict["values"]:
            if 1 <= entry[0] <= 12 and entry[1]:
                locDate = datetime(year, entry[0], 1)
                value = entry[1] * 1000
                dataframe_generation = dataframe_generation.append(
                    pd.DataFrame({'year': year, 'technology': newFueltype, 'loctimestamp': locDate, 'actual': value},
                                 index=[0]), ignore_index=True)
    year = year + 1
dataframe_generation = dataframe_generation[["year", "technology", "loctimestamp", "actual"]]

# Import to db
dataframe_generation.to_sql(name='generation_ise', con=cnx, if_exists='append', index=False)
print(dataframe_generation)
