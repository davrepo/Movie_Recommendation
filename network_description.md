# Movie Recommendation System and User Attribute Analysis - Network description
This  network represents 100,000 user–movie ratings from http://movielens.umn.edu/. 

## Basic Network Description
The network is bipartite - left partition represents users of *movielens.org* site and right partition represents movies. 
An edge between a user and a movie represents the rating of the movie by that user. Edges are undirected and weighted - 
the weight of an edge represents the number of stars that the user gave to the movie. Edge weights are integers 
in the range 1-5 (where 1 is the worst rating and 5 is the best rating a movie can get)

<!-- 7 by 2 table -->
| Network Properties | Values |
|--------------------| --- |
| Network Format     | Bipartite, undirected |
| Left Partition     | Users |
| Right Parititon    | Movies |
| Edge Meaning       | Rating of movie by user |
| Edge Type          | Ratings, no multiple edges |
| Temporal Data      | Edges are annotated with timestamps |


## Data Source
This dataset was collected by GroupLens Research at the University of Minnesota from the 
[MovieLens](https://movielens.org) website. It was collected during the seven-month period from September 19th 1997 
through April 22nd 1998. 

The data has been cleaned up before release - users who had less than 20 ratings or did not have complete 
demographic information were removed from this dataset. 

Network Dataset Link: [Source](http://konect.cc/networks/movielens-100k_rating/)



