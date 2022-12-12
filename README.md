# si507FinalMovies

Packages required: bs4, requests, csv, urllib.request, PIL, matplotlib (updated to most recent update)

API Key information: Although this is bad practice, the API key that I generated for OMDB is hardcoded. If you wanted to get your own API key for OMDB you would go to http://www.omdbapi.com/apikey.aspx and request your own. 

# Data Structure Information

I chose to use a tree to help structure my data for building this recommendation system. I made a tree recommendation structure with 3 levels. The tree nodes  consist of lists of the movies that fit the criteria that have been requested by the answers to the following questions.

The questions that determine the three layers of the tree are: 
Do you want to watch something family friendly? (rated G/PG) (yes/no)
Do you want to watch something over 100 minutes? (yes/no)
Do you want to watch a movie that is over 15 years old? (yes/no)

Since the questions all are checking unrelated factors and involve running through the list of movies to group them indivually by if they follow the criteria or not, I made the trees non-recursively. If there were more than 3 layers/100 movies, I would definitely try to figure out another strategy for recursively adding the data in. 

# How to run the program 

Run the file, movieGenerator.py, and follow the prompts that are asked. There are three important factors you will be asked about. 

The first factor considers how specific of a recommendation you want. There are three levels of the tree that was generated and you can get a recommendation at any level. The first question will be "Do you want a family friendly movie?". The second is "Do you want to watch something over 100 minutes?". The third is "Do you want to watch a movie that is over 15 years old?". So, if you say that you want only to consider the first question into your recommendation, you will be choosing from either family friendly (PG/G) or not family friendly (PG-13/R/Not rated) movies. However, if you say you want to consider all three, your recommendation will take your answers to all three questions into account. 

The second major factor of the recommendation system is if you want the movie to be randomly selected for you or not.

This answer slightly modifies the third factor of this recommendation which is what the visualization output is. 

If you want a randomly selected movie, you have two visualization options, which are:
1. The poster, a graph of ratings, and the plot & critic consensus of one random movie that fit your criteria
2. Three randomly selected movie posters that fit your criteria.

If you want to pick the movie by title, you have five visualization options, which are: 
1. The movie poster
2. A graph of the movie's ratings
3. The plot & critic consensus of the selected movie
4. A prompt to the command line with all of the information collected from the API about the movie
5. The poster, a graph of ratings, and the plot & critic consensus of the movie

