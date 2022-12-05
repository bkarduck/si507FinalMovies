from bs4 import BeautifulSoup
import requests
import csv

url = "https://editorial.rottentomatoes.com/guide/best-disney-movies-to-watch-now/"
resp = requests.get(url)
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
        movieDict['Release Year'] = movieText[1][:4]
        movieDict['Critic Consensus'] = tags2[i].contents[3].text.split(': ')[1]
        movieDict["Rank"] = int(tags[i].text[1:])
        movieDict['Director'] = tags2[i].contents[9].text.split(': ')[1]
        #movieDict['Start Year'] = tag.span.subtle.start-year.text
        movieList.append(movieDict)
print(len(movieList))

filename = 'scrapingData.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['Title','Release Year','Critic Consensus','Rank','Director'])
    w.writeheader()
    for movie in movieList:
        w.writerow(movie)
f.close()

