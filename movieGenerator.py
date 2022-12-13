from bs4 import BeautifulSoup
import requests
import csv
import json
import random
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

url = "https://editorial.rottentomatoes.com/guide/best-disney-movies-to-watch-now/"
resp = requests.get(url)

def rottenTomatoScrape():
    ''' Scrapes the Rotten Tomatoes website for the best Disney movies
    to watch, cleans the data, and appends information about each movie
    to a list of movies. 
    Parameters
    ----------
    None
    Returns
    -------
    The list of dictionaries of movies generated from the parsing
    '''
    movieList = []
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser')
        tags = soup.find_all('div', class_='countdown-index')
        tags2 = soup.find_all('div', class_= 'col-sm-24')
        tags3 = soup.find_all('h2')
                    
                        
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


def scrapingCSVWriter(movieList):
    ''' opens the scrapingData CSV file and writes the movies from 
    the Rotten Tomatoes movie list into the CSV
    Parameters
    ----------
    None
    Returns
    -------
    None
    '''
    with open('scrapingData.csv', 'w', newline='') as f:
        w = csv.DictWriter(f,['Title','Release Year','criticConsensus','Rank','Director'])
        w.writeheader()
        for movie in movieList:
            w.writerow(movie)
    f.close()

baseurl = "http://www.omdbapi.com/"

overallMovie = []

def getAPIData(movieList):
    ''' Takes the movies from the Rotten Tomatoes scraped list and calls the 
    OMDB API on each title. Then, it cleans the data and organizes it for use
    in a tree by appending information about each movie to a list of movies. 
    Parameters
    ----------
    None
    Returns
    -------
    The list of dictionaries of movies generated from the parsing
    '''
    for movie in movieList:
        movieInfoDict = {}
        parameter_dictionary = {'t': movie['Title'],'plot': 'full', 'apikey': "5828b360"}
    
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
        movieInfoDict['Poster'] = response_json['Poster']
        overallMovie.append(movieInfoDict)
    return overallMovie
    

def apiCSVWriter(overallMovie):
    ''' opens the apiData CSV file and writes the movies from 
    the API Data overall movie list into the CSV file
    Parameters
    ----------
    None
    Returns
    -------
    None
    '''
    with open('apiData.csv', 'w', newline='') as f:
        w = csv.DictWriter(f,['Title','Year', 'Rated','Runtime','Genre','Director','Plot','rottenTomatoes','imdbRating','Metascore', 'BoxOffice', 'imdbVotes','criticConsensus','Rank', 'Poster'])
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
        
    except:
        movieList = []
    return movieList


def saveTree(cache_dict, filename):
    ''' saves the tree as a json file
    Parameters
    ----------
    tree: dict
        The dictionary (tree) to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(filename,"w")
    fw.write(dumped_json_cache)
    fw.close() 

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
    else:
        confirmQuestion = input(f'{text}')
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


def createRatingTree(movieList):

    '''
    Creates a tree based on the film's ratings

            Parameters:
                    movieList (list): A list of dictionaries of the movies
            Returns:
                    firstLayerTree (list): a tree of the data after being split up
                    
    '''
    
    text = "Do you want to watch something family friendly? (yes/no - no also returns films that don't have a rating): "
    left, right = splitByRatings(movieList)
    
    firstLayerTree = text, left, right
    return firstLayerTree

def createTimeTree(firstTree):
    '''
    Creates a tree based on the film's length

            Parameters:
                    firstTree (list): A list of list of tuples
            Returns:
                    secondLayerTree (list): a tree of the data after being split up by movie length
                    
    '''
    text, left, right = firstTree
    newQuestion = "Do you want to watch something over 100 minutes? (yes/no): "
    
    leftT, rightT = splitByTime(text)
    

    secondLayerTree = newQuestion, leftT, rightT
    return secondLayerTree

def createReleaseDateTree(secondTree):
    '''
    Creates a tree based on the film's release date

            Parameters:
                    secondTree (list): A list of list of tuples
            Returns:
                    thirdLayerTree (list): a tree of the data after being split up by the release date
                    
    '''
    text, left, right = secondTree
    newQuestion = "Do you want to watch a movie that is over 15 years old? (yes/no): "
    
    leftT, rightT = splitByReleaseDate(left[0])
    leftTree = newQuestion, leftT, rightT
    leftT, rightT = splitByReleaseDate(right[0])
    rightTree = newQuestion, leftT, rightT

    thirdLayerTree = text, leftTree, rightTree
    return thirdLayerTree
    
def splitByRatings(movieList):
    ''' Splits the movies in a given movie list based on ratings
    Parameters
    ----------
    movieList: list of dictionaries
        The list of movies to parse through and split up
    Returns
    -------
    left, right: tuples
        Left and right tree leaves that have been sorted appropriately
    '''
    
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
    ''' Splits the movies in a given movie list based on movie length
    Parameters
    ----------
    movieList: list of dictionaries
        The list of movies to parse through and split up
    Returns
    -------
    left, right: tuples
        Left and right tree leaves that have been sorted appropriately
    '''
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
    ''' Splits the movies in a given movie list based on movie release date
    Parameters
    ----------
    movieList: list of dictionaries
        The list of movies to parse through and split up
    Returns
    -------
    left, right: tuples
        Left and right tree leaves that have been sorted appropriately
    '''
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


def graphPoster(selectedMovie):
    ''' graphs the given movie poster
    Parameters
    ----------
    selectedMovie: dict
        The dictionary for the movie to generate the poster from
    Returns
    -------
    None
    '''
    urllib.request.urlretrieve(selectedMovie['Poster'], 'movie.png')
  
    img = Image.open("movie.png")
    f, a0 = plt.subplots(1, 1)
    plt.suptitle(f'Your movie is: {selectedMovie["Title"]}', y=.96, weight='bold')
    f.set_figheight(6)
    f.set_figwidth(8)
    a0.imshow(img, zorder=1)
    a0.yaxis.set_visible(False)
    a0.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
    plt.show()

def graphMovieRatings(selectedMovie):

    ''' graphs the given movie ratings (Rotten Tomatoes, IMDB, Metascore, 
    and an average of the three scores)
    Parameters
    ----------
    selectedMovie: dict
        The dictionary for the movie to generate the graph from
    Returns
    -------
    None
    '''

    if '%' in selectedMovie["rottenTomatoes"]:
        rottenTom = float(selectedMovie["rottenTomatoes"].split('%')[0])
    elif '/' in selectedMovie['rottenTomatoes']:
        rottenTom = float(selectedMovie["rottenTomatoes"].split('/')[0])
    imdbRating = float(selectedMovie['imdbRating']) * 10
    metascore = float(selectedMovie['Metascore'])
    averageScore = (rottenTom + imdbRating + metascore) / 3

    xAxis = ['Rotten Tomatoes', 'IMDB', 'Metascore', 'Average Rating']
    yAxis = [rottenTom, imdbRating, metascore, averageScore]
    colors = ['firebrick', 'goldenrod', 'green', 'slategrey']
    f, a0 = plt.subplots(1, 1)
    plt.suptitle(f'Your movie is: {selectedMovie["Title"]}', y=.96, weight='bold')
    f.set_figheight(6)
    f.set_figwidth(8)
    bars = a0.bar(xAxis, yAxis, color = colors)
    a0.set_title(f'Ratings')
    a0.set_ylabel('Ratings out of 100')
    a0.set_xlabel('Rating Platform')
    a0.set_ybound(0, 100)
    a0.bar_label(bars)
    plt.show()

def graphBoxDescription(selectedMovie):
    ''' Displays the plot and critic review of the given movie 
    Parameters
    ----------
    tree: dict
        The dictionary for the movie to generate the information from
    Returns
    -------
    None
    '''
    f, a0 = plt.subplots(1, 1)
    plt.suptitle(f'Your movie is: {selectedMovie["Title"]}', y=.96, weight='bold')
    f.set_figheight(6)
    f.set_figwidth(8)
    a0.axis('off')
    txt = a0.text(0.5, 0.98, f'Rating: {selectedMovie["Rated"]}  ||  Runtime: {selectedMovie["Runtime"]} minutes. \n\nPlot: {selectedMovie["Plot"]} \n\nCritic Consensus: {selectedMovie["criticConsensus"]}', fontsize=10, transform=a0.transAxes, horizontalalignment='center',
        verticalalignment='top', wrap = True, bbox=dict(facecolor='lavender', alpha=0.4))
    a0.set_title(f'Description', loc='center')
    txt._get_wrap_line_width = lambda : 900.
    plt.show()
   
def graphAllMovieDetails(selectedMovie):
    ''' Displays the graph of the given movie's ratings (Rotten Tomatoes, IMDB, Metascore, 
    and an average of the three scores), the movie poster, and the 
    plot and critic review of the given movie 
    Parameters
    ----------
    tree: dict
        The dictionary for the movie to generate the information from
    Returns
    -------
    None
    '''
    urllib.request.urlretrieve(selectedMovie['Poster'], 'movie.png')
  
    img = Image.open("movie.png")

    if '%' in selectedMovie["rottenTomatoes"]:
        rottenTom = float(selectedMovie["rottenTomatoes"].split('%')[0])
    elif '/' in selectedMovie['rottenTomatoes']:
        rottenTom = float(selectedMovie["rottenTomatoes"].split('/')[0])
    imdbRating = float(selectedMovie['imdbRating']) * 10
    metascore = float(selectedMovie['Metascore'])
    averageScore = (rottenTom + imdbRating + metascore) / 3

    xAxis = ['Rotten Tomatoes', 'IMDB', 'Metascore', 'Average Rating']
    yAxis = [rottenTom, imdbRating, metascore, averageScore]
    colors = ['firebrick', 'goldenrod', 'green', 'slategrey']
    
    f, (a0, a1, a2) = plt.subplots(1, 3, width_ratios=[2, 1, 1.75])
    plt.subplots_adjust(left=0.08,top=0.9,right=0.92,bottom=0.1)
    plt.suptitle(f'Your movie is: {selectedMovie["Title"]}', y=.96, weight='bold')
    f.set_figheight(8)
    f.set_figwidth(13)

    bars = a0.bar(xAxis, yAxis, color = colors)
    a0.set_title(f'Ratings')
    a0.set_ylabel('Ratings out of 100')
    a0.set_xlabel('Rating Platform')
    a0.set_ybound(0, 100)
    a0.bar_label(bars)

    a1.imshow(img, zorder=1)
    a1.yaxis.set_visible(False)
    a1.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
    a1.set_xlabel(f'Genre(s): {selectedMovie["Genre"]}')

    a2.axis('off')
    txt = a2.text(0.02, 0.98, f'Rating: {selectedMovie["Rated"]}  ||  Runtime: {selectedMovie["Runtime"]} minutes. \n\nPlot: {selectedMovie["Plot"]} \n\nCritic Consensus: {selectedMovie["criticConsensus"]}', fontsize=10, transform=a2.transAxes, horizontalalignment='left',
        verticalalignment='top', wrap = True, bbox=dict(facecolor='lavender', alpha=0.4))
    a2.set_title(f'Description', loc='center')
    txt._get_wrap_line_width = lambda : 675.

    plt.show()

def graph3Posters(selectedMovies):
    ''' graphs the movie posters for the three selected movies
    Parameters
    ----------
    selectedMovies: list of dictionaries
        The list of dictionaries of the movies to generate the posters from
    Returns
    -------
    None
    '''
    count = 1
    for movie in selectedMovies:
        urllib.request.urlretrieve(movie['Poster'], f'movie{count}.png')
        count += 1
    
    img1 = Image.open("movie1.png")
    img2 = Image.open("movie2.png")
    img3 = Image.open("movie3.png")
    f, (a0, a1, a2) = plt.subplots(1, 3)
    f.set_figheight(8)
    f.set_figwidth(13)
    plt.suptitle(f'Your movies are: {selectedMovies[0]["Title"]}, {selectedMovies[1]["Title"]}, and {selectedMovies[2]["Title"]}', y=.96, weight='bold')

    a0.set_title(f'{selectedMovies[0]["Title"]}')
    a0.imshow(img1, zorder=1)
    a0.yaxis.set_visible(False)
    a0.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)

    a1.set_title(f'{selectedMovies[1]["Title"]}')
    a1.imshow(img2, zorder=1)
    a1.yaxis.set_visible(False)
    a1.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)

    a2.set_title(f'{selectedMovies[2]["Title"]}')
    a2.imshow(img3, zorder=1)
    a2.yaxis.set_visible(False)
    a2.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)

    plt.show()

def main():

    print('Welcome to the Disney Plus Movie Generator!')
    print('This program will help you find a great movie from a recent Rotten Tomatoes list of the best Disney Plus offerings')       
    overallMovieList = open_cache('apiData.csv')
    if len(overallMovieList) == 0:
        scrapingData = open_cache('scrapingData.csv')
        if scrapingData == []:
            scrapingData = rottenTomatoScrape()
            scrapingCSVWriter(scrapingData)
        overallMovieList = getAPIData(scrapingData)
        apiCSVWriter(overallMovieList)
    
    tree1 = createRatingTree(overallMovieList)
    text, left, right = tree1
    treeL = createTimeTree(left)
    treeR = createTimeTree(right)
    tree2 = tree1[0], createTimeTree(left), createTimeTree(right)
    treeL2 = createReleaseDateTree(treeL)
    treeR2 = createReleaseDateTree(treeR)
    tree3 = text, treeL2, treeR2

    treeFile = "savedTree.json"
    saveTree(tree3, treeFile)
    numOfQuestions = input("How specific do you want your recommendation to be? Enter '1' to answer 1 question, '2' to answer 2 questions, and '3' to answer 3 questions to narrow down your selection: ")

    if numOfQuestions == "1":
        treeToPlay = tree1
    elif numOfQuestions == "2":
        treeToPlay = tree2
    elif numOfQuestions == "3":
        treeToPlay = tree3
    else:
        treeToPlay = tree3


    playTree = simplePlay(treeToPlay)

    lengthOfOptions = len(playTree)
    randomOrNo = input(f'Do you want to have a movie chosen at random for you from the {lengthOfOptions} options? Enter "yes" if so, otherwise type anything else: ' )
    if randomOrNo == 'yes':
        postersOrGraph = input('Would you rather see three random movie posters that fit your criteria or see the details about a specific movie? Enter 1 to see three posters and 2 to see information on a singular movie: ')
        if postersOrGraph == "1":
            selectedMovies = random.choices(playTree, k=3)
            graph3Posters(selectedMovies)
        elif postersOrGraph == "2": 

            selectedMovie = random.choice(playTree)
            graphAllMovieDetails(selectedMovie)
        else:
            print("You entered something other than 1 or 2, however, you get a random choice anyways. Enjoy!")
            selectedMovie = random.choice(playTree)
            graphAllMovieDetails(selectedMovie)
    else:
        dictOfTitles = {}
        count = 1
        
        for movie in playTree:

            dictOfTitles[count] = (movie['Title'])
            count += 1
        print('The movies that fit your criteria are:')
        print(dictOfTitles)
        doneLooking = False
        while doneLooking == False:
            movieNum = input("Select the number of the movie you want to see more information on (if an eligible number is not selected, a movie will be chosen at random for you): ")
            outputOption = input("Do you want to see 1. Only the movie poster? 2. Only the movie rating? 3. Only the movie plot and critic review? 4. A prompt to the command line with all of the information about the movie 5. A combination display of the graph of ratings, poster, and plot/critic consensus Enter the number of the option you want (if anything else is entered, the poster, graph of ratings, and description will be displayed): ")

            if int(movieNum) in dictOfTitles.keys():
                movieNum = int(movieNum) - 1
            else:
                movieNum = random.choice(range(0, lengthOfOptions-1))
            
            if outputOption == '1':
                graphPoster(playTree[movieNum])

            elif outputOption == '2':
                graphMovieRatings(playTree[movieNum])

            elif outputOption == '3':
                graphBoxDescription(playTree[movieNum])

            elif outputOption == '4':
                print(playTree[movieNum])
            else:
                graphAllMovieDetails(playTree[movieNum])
            notFinished = input("Do you want to see information about another movie? Enter yes if so. Entering anything else will end the program. ")
            if notFinished != "yes":
                doneLooking = True
    print("Enjoy the movie!")

if __name__ == "__main__":
    main()
    

