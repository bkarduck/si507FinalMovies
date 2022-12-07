from bs4 import BeautifulSoup
import requests
import csv
import json

url = "https://editorial.rottentomatoes.com/guide/best-disney-movies-to-watch-now/"
resp = requests.get(url)

def rottenTomatoScrape():
    movieList = []
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser')
        tags = soup.find_all('div', class_='countdown-index')
        tags2 = soup.find_all('div', class_= 'col-sm-24')
        tags3 = soup.find_all('h2')
        #tags = soup.find_all('h2', class_='c-gallery-vertical-slide__title')
        #<h2 class="c-gallery-vertical-slide__title">“10 Things I Hate About You” (1999)</h2>
        # <div class="row countdown-item-details">
                    
                        
        for i in range(len(tags)):
            movieDict = {}
            movieText = tags3[i].text.split("(")
            movieDict['Title'] = tags3[i].a.text
            if movieDict['Title'] == "Marvel's the Avengers":
                movieDict['Title'] = 'The Avengers'
            movieDict['Release Year'] = movieText[1][:4]
            movieDict['criticConsensus'] = tags2[i].contents[3].text.split(': ')[1]
            movieDict["Rank"] = int(tags[i].text[1:])
            movieDict['Director'] = tags2[i].contents[9].text.split(': ')[1]
            #movieDict['Start Year'] = tag.span.subtle.start-year.text
            movieList.append(movieDict)
    return movieList



def scrapingCSVWriter( movieList):
    with open('scrapingData.csv', 'w', newline='') as f:
        w = csv.DictWriter(f,['Title','Release Year','criticConsensus','Rank','Director'])
        w.writeheader()
        for movie in movieList:
            w.writerow(movie)
    f.close()
#scrapingCSVWriter(filename, rottenTomatoScrape())

API = "http://www.omdbapi.com/?apikey=&126cef76"
baseurl = "http://www.omdbapi.com/"


overallMovie = []
# Rated, Runtime, Genre, Plot, Poster, 
# Ratings (list) -> Internet Movie Database x/10, Rotten Tomatoes x%, Metacritic x/100... 
# Metascore, imdbRating, imdbVotes, BoxOffice
def getAPIData(movieList):
    for movie in movieList:
        movieInfoDict = {}
        parameter_dictionary = {'t': movie['Title'], 'apikey': "5828b360"}
    
        response = requests.get(baseurl, parameter_dictionary)
        response_json = response.json()
        movieInfoDict['Title'] = response_json['Title']
        movieInfoDict['Year'] = int(response_json['Year'][:4])
        movieInfoDict['Rated'] = response_json['Rated']
        if response_json['Runtime'] == 'N/A':
            movieInfoDict['Runtime'] = 60
        else:
            movieInfoDict['Runtime'] = int(response_json['Runtime'].split(' ')[0])
        movieInfoDict['Genre'] = response_json['Genre']
        movieInfoDict['Director'] = movie['Director']
        movieInfoDict['Plot'] = response_json['Plot']
        if len(response_json['Ratings']) > 1:
            movieInfoDict['rottenTomatoes'] = response_json['Ratings'][1]["Value"]
        else:
            movieInfoDict['rottenTomatoes'] = "N/A"
        movieInfoDict['imdbRating'] = response_json['imdbRating']
        movieInfoDict['Metascore'] = response_json['Metascore']
        if response_json['Type'] == 'series':
            movieInfoDict['BoxOffice'] = 'N/A'
        else:
            movieInfoDict['BoxOffice'] = response_json['BoxOffice']
        movieInfoDict['imdbVotes'] = response_json['imdbVotes']
        movieInfoDict['criticConsensus'] = movie['criticConsensus']
        movieInfoDict['Rank'] = movie['Rank']
        overallMovie.append(movieInfoDict)
    return overallMovie
    

def apiCSVWriter(overallMovie):
    with open('apiData.csv', 'w', newline='') as f:
        w = csv.DictWriter(f,['Title','Year', 'Rated','Runtime','Genre','Director','Plot','rottenTomatoes','imdbRating','Metascore', 'BoxOffice', 'imdbVotes','criticConsensus','Rank'])
        w.writeheader()
        for movie in overallMovie:
            w.writerow(movie)
    f.close()

def open_cache(filename):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            movieList = list(csv_reader)
        #cache_dict = json.loads(cache_contents)
        
    except:
        movieList = []
    return movieList

overallMovieList = open_cache('apiData.csv')
if len(overallMovieList) == 0:
    scrapingData = open_cache('scrapingData.csv')
    if scrapingData == []:
        scrapingData = rottenTomatoScrape()
        scrapingCSVWriter(scrapingData)
    overallMovieList = getAPIData(scrapingData)
    apiCSVWriter(overallMovieList)
#print(overallMovieList)



def save_cache(cache_dict, filename):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(filename,"w")
    fw.write(dumped_json_cache)
    fw.close() 



# Do you want to watch a family friendly movie (G/PG)
# Do you want to watch a movie that's over 100 minutes
# Do you want to watch something more than 15 years old? Before 2008
# What Genre are you interested in?

def simplePlay(tree):
    
    '''
    Plays tree for any situation that only involves a yes or no answer.

            Parameters:
                    tree (list): A list of list of tuples
                  

            Returns:
                    playLeaf(tree) (bool): true or false depending on yes or no answer
                    simplePlay(left/right): recursively calls simplePlay depending on yes or no answer
    '''

    text, left, right = tree
    if isLeaf(tree):
        return text
        #return playLeaf(tree)
    else:
        confirmQuestion = input(f'{text} (yes/no) ')
        if confirmQuestion == 'yes':
            return simplePlay(left)
        elif confirmQuestion == 'no':
            return simplePlay(right)

def isLeaf(tree):

    '''
    Determines if node has children.

            Parameters:
                    tree (list): A list of list of tuples
                  

            Returns:
                    True/False (bool): true or false depending if node has children
    '''
    text, left, right = tree
    if left is None and right is None:
        return True
    else:
        return False

def playLeaf(tree):
    '''
    Confirms if the leaf node is a certain string object.

            Parameters:
                    tree (list): A list of list of tuples
                  

            Returns:
                    True/False (bool): true or false depending on yes or no answer inputted by human
    '''
    text, left, right = tree
    confirmObject = input(f'Is the object {text[0]}? (yes/no) ')
    if confirmObject == 'yes':
        return True
            
    elif confirmObject == 'no':
        return False


def createRatingTree(movieList):
    
    text = "Do you want to watch something family friendly (yes/no)?"
    left, right = splitByRatings(movieList)
    
    firstLayerTree = text, left, right
    return firstLayerTree

def createTimeTree(firstTree):
    text, left, right = firstTree
    newQuestion = "Do you want to watch something over 100 min (yes/no)?"
    
    leftT, rightT = splitByTime(text)
    

    secondLayerTree = newQuestion, leftT, rightT
    return secondLayerTree

def createReleaseDateTree(secondTree):
    text, left, right = secondTree
    newQuestion = "Do you want to watch a movie that is over 15 years old (yes/no)?"
    
    leftT, rightT = splitByReleaseDate(left[0])
    leftTree = newQuestion, leftT, rightT
    leftT, rightT = splitByReleaseDate(right[0])
    rightTree = newQuestion, leftT, rightT


    
    
    thirdLayerTree = text, leftTree, rightTree
    return thirdLayerTree
    
def splitByRatings(movieList):
    leftList = []
    rightList = []
    for movie in movieList:
        if movie["Rated"] == 'G' or movie["Rated"] == 'PG':
            leftList.append(movie)
        else:
            rightList.append(movie)
    left = (leftList, None, None)
    right = (rightList, None, None)
    return left, right

def splitByTime(movieList):
    leftList = []
    rightList = []
    for movie in movieList:
        if int(movie["Runtime"]) >= 100:
            leftList.append(movie)
        else:
            rightList.append(movie)
    left = (leftList, None, None)
    right = (rightList, None, None)
    return left, right

def splitByReleaseDate(movieList):
    leftList = []
    rightList = []
    for movie in movieList:
        if int(movie["Year"]) < 2008:
            leftList.append(movie)
        else:
            rightList.append(movie)
    left = (leftList, None, None)
    right = (rightList, None, None)
    return left, right
    


listy = [{'Ratings': 'G', 'Runtime': 90, 'releaseYear': 2005},
{'Ratings': 'G', 'Runtime': 90, 'releaseYear': 2015},
{'Ratings': 'PG', 'Runtime': 120, 'releaseYear': 2015},
{'Ratings': 'PG-13', 'Runtime': 90, 'releaseYear': 2005},
{'Ratings': 'R', 'Runtime': 100, 'releaseYear': 2003},
{'Ratings': 'G', 'Runtime': 130, 'releaseYear': 2005},
{'Ratings': 'PG', 'Runtime': 90, 'releaseYear': 2018},
{'Ratings': 'R', 'Runtime': 120, 'releaseYear': 2020},
{'Ratings': 'R', 'Runtime': 130, 'releaseYear': 2015},
{'Ratings': 'PG-13', 'Runtime': 140, 'releaseYear': 2017},
{'Ratings': 'R', 'Runtime': 90, 'releaseYear': 2005}

]

tree1 = createRatingTree(overallMovieList)
text, left, right = tree1
treeL = createTimeTree(left)
treeR = createTimeTree(right)
t2, l2, r2 = treeL
tree2 = tree1[0], createTimeTree(left), createTimeTree(right)
treeL2 = createReleaseDateTree(treeL)
treeR2 = createReleaseDateTree(treeR)
tree3 = text, treeL2, treeR2
#print(tree3)
y = simplePlay(tree3)
print(len(y))


## idea: make a class that stores values per movie and has the functions that split the lists
