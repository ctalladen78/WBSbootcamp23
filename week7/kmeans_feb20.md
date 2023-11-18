
#### task : label df with num clusters

* use audio_5k.csv

* elbow method

* silhouette score

* cluster exploration
- univariate and bivariate exploration of cluster
- Plotting the distribution of an individual feature (such as “energy”) across different clusters.
- Visualizing the clusters in a scatterplot with two different features.


Other interesting tasks you might want to perform in terms of cluster exploration include:

- manual labeling using cluster id
- Looking at the size of the clusters (how many observations do they have?)
- Listening to a few songs from each cluster to get a feeling for what do these clusters contain.

#### presentation
business questions

* Are Spotify's audio features able to identify 'similar songs', as defined by humanly detectable criteria?
There are non-human detectable features that could be relevant to classification (bpm, acoustics, background beats)


* Is K-Means a good method to create playlists?
Drawbacks of kmeans for classification use cases

#### Slides
* Data preparation:
Reading the data
Exploration (understanding of features)
Dropping unwanted features

* Modelling:
Data scaling (potentially, other transformations)
K-Means exploration of clusters (elbow method, silhouette coefficient…)
K-Means final model

* Cluster exploration:
Univariate and bivariate exploration of the clusters
Manual labelling of the clusters



