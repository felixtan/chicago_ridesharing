# Feature selection
## Strategy
feature selection 
* omit cols missing over 30% of data
* omit pickup and dropoff centroid location cols 
    * because the data's already represented by lat/longs
* omit census tracts because they aren't meaningful in everyday parlance and the given numbers don't match up to census tract numbers given [here](https://www.chicagorealtor.com/realtor-tools/neighborhood-information/census-track-maps/)
* use pickup/dropoff community area as the only location cols
    * k-means isn't good with lat/long data (or categorical)
    * can be categorized

## Feature actions (besides handling missing values)
* Trip ID: (how to handle ids?)
* Trip Start Timestamp: use to calculate/categorize time of day
* Trip End Timestamp: use to calculate/categorize time of day
* Trip Seconds: convert to minutes
* Trip Miles: use as is
* Pickup Census Tract: omit
* Dropoff Census Tract: omit
* Pickup Community Area: categorize, set to 'Outside of Chicago' if empty
* Dropoff Community Area: categorize, set to 'Outside of Chicago' if empty
* Fare: use as is
* Tip: use as is
* Additional Charges: use as is
* Trip Total: use as is
* Shared Trip Authorized: categorize
* Trips Pooled: use as is
* Pickup Centroid Latitude: omit
* Pickup Centroid Longitude: omit
* Pickup Centroid Location: omit
* Dropoff Centroid Latitude: omit
* Dropoff Centroid Longitude: omit
* Dropoff Centroid Location: omit

## Categories
* Trip Start/End
    * Morning: 6:30AM - 12PM
    * Afternoon: 12PM - 6PM
    * Evening: 6PM - 11:30PM
    * Night: 11:30PM - 6:30AM
* Pickup/Dropoff Community Area: map codes to neighborhood/community names, empty = "Outside Chicago"
* Shared Trip Authorized: true or false

## Issues
Location (dropoff/pickup) values are empty for locations outside of Chicago
* ~~could classify locations as (inside Chicago, outside Chicago)~~
    * but this elminates the possibility of answering "where in Chicago" questions like "where in Chicago can I get the highest fares?"
* [k-means is not fit for handling geospatial data](https://datascience.stackexchange.com/questions/761/clustering-geo-location-coordinates-lat-long-pairs)
    * k-means relies on euclidean distance
* [k-means isn't good for categorical data either](https://www.researchgate.net/post/What_is_the_best_way_for_cluster_analysis_when_you_have_mixed_type_of_data_categorical_and_scale)
    * either have to choose an algorithm that can handle mixed numerical/categorical or find a meaningful distance metric for categorical data
    * k-means relies on euclidean distance
        * gower distance "behaves like euclidean"  
* how to deal with timestamps?
    * can't leave as is because time since 1970 doesn't make sense unless maybe you're doing time series
    * for this dataset, i'm thinking of transforming to time/hour of day
    * if it was a year's worth of data, could be transformed to month

## Data notes
[Community areas in Chicago are coded, numbered areas](https://en.wikipedia.org/wiki/Community_areas_in_Chicago)
* difference with counties?

## Clustering goals
For riders: 
* tip: where can I get the highest/most frequest tips?
* payoff: how can I get the best fare/trip miles ratio?

For investors
* ?

For regulators/govt:
* ?

## Things learned
### Pandas
[removing cols from a dataframe](https://stackoverflow.com/questions/14940743/selecting-excluding-sets-of-columns-in-pandas)
[appending rows to a dataframe (probably use .loc())](https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe)

## Techniques
[sample a subset of the data using skiprows arg of pandas.read_csv for faster exploration](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
specify dtypes on load to reduce memory footprint

### ML
[k-means is not fit for handling geospatial data](https://datascience.stackexchange.com/questions/761/clustering-geo-location-coordinates-lat-long-pairs)
[k-means relies on euclidean distance only](https://stackoverflow.com/questions/5529625/is-it-possible-to-specify-your-own-distance-function-using-scikit-learn-k-means)
* this means that the data values have to have relative numerical meaning 
    * categorical values dont have this since they're jsut dummy values with equal meaning
    * lat/long values don't have this since they represent points on the globe

gower distance seems to be the most popular distance metric for mixed numerical and categorial data
* measures similiarity between rows
* [poster denis seems to have made a PR to sklearn to provide gower distance](https://stackoverflow.com/questions/5529625/is-it-possible-to-specify-your-own-distance-function-using-scikit-learn-k-means)
* [his code](https://sourceforge.net/projects/gower-distance-4python/)

[PAM clustering and silhoutte coefficient can be used for mixed data](https://towardsdatascience.com/clustering-on-mixed-type-data-8bbd0a2569c3)

[nice explanation of the gower distance](https://stats.stackexchange.com/questions/15287/hierarchical-clustering-with-mixed-type-data-what-distance-similarity-to-use)
* uses a different metric udnerneath for each type of variable then composes them
* "behaves like the euclidean distance", so therefore can be used with k-means
    * I'm just taking this guy's word for it 

### To read
[scikit-learn lab: utils that make it easier to run common sklearn experiments](https://scikit-learn-laboratory.readthedocs.io/en/latest/)
[https://pbpython.com/categorical-encoding.html]
How to preprocess timestamp data

### Sources
* [average sleep duration is 7 hours](https://news.gallup.com/poll/166553/less-recommended-amount-sleep.aspx)
    * use to make decision about trip start/end time of day categories
* [average bedtime is 11:30pm](https://www.homes.com/blog/2016/12/what-time-does-america-go-to-bed/)
    * use to make decision about trip start/end time of day categories