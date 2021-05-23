#https://bit.ly/2NyxdAG
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.imdb.com/search/title/?title_type=feature&primary_language=te&sort=num_votes,desc&view=advanced&start=%s'
movies = []
start = 1
index = 1

def add_movies_from_url(url):
    global movies, start, index
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    movies_list = soup.find("div", class_="lister-list")
    movies_list = movies_list.find_all("div", class_="lister-item-content")

    for movie in movies_list:
        name, director, actors, popularity, year, rating = None, None, [], None, None, None 
        try:
            popularity = index
            try:
                year = movie.find_all('span')[1].text[1:-1]
            except:
                pass
            try:
                rating = movie.find('strong').text
            except:
                pass
            try:
                name = movie.find('a').text
            except:
                pass
            try:
                people = movie.find_all('p')[2].find_all('a')
            except:
                pass
            try:
                director = people[0].text
            except:
                pass

            actors = [person.text for person in people[1:]] if len(people)>1 else []
        except Exception as e:
            print('Failed for - ', index, name)

        movies.append([popularity, year, rating, name, director, actors])
        index+=1
    print('Done for the url - ', url)

for i in range(100):
    add_movies_from_url(url%start)
    start+=50

columns = ["popularity", "year", "rating", "name", "director", "actors"]
df = pd.DataFrame(movies, columns=columns)
df.to_csv("more_info.csv", index=False)
