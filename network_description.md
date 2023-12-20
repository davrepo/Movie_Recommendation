# Movie Recommendation System and User Attribute Analysis - Network description
This  network represents 100,000 user–movie ratings from http://movielens.umn.edu/. 

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

## Additional Data
There are additional data included with this dataset - about both users and movies.

### Users
There are demographic information about the users included:
* age
* gender
* occupation - list of possible occupations can be found in file *u.occupation*
* zip code

They can be found in *u.user* file and are associated with corresponding user id.

### Movies
There are information about the movies included:
* movie title 
* release date 
* video release date - missing for a lot of movies, so we decided to drop this column
* IMDb URL - missing for some movies and irrelevant for our analysis, so we decided to drop this column
* genre - there are 19 possible genres and 19 columns corresponding to them (they can be found in file *u.genre*). 1 indicates the movie
              is of that genre, a 0 indicates it is not; movies can be in several genres at once

They can be found in *u.item* file and are associated with corresponding movie id. 

## Data Source
This dataset was collected by GroupLens Research at the University of Minnesota from the 
[MovieLens](https://movielens.org) website. It was collected during the seven-month period from September 19th 1997 
through April 22nd 1998. 

The data has been cleaned up before release - users who had less than 20 ratings or did not have complete 
demographic information were removed from this dataset. 

Network Dataset Link: [Source](http://konect.cc/networks/movielens-100k_rating/)



