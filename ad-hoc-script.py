from requests import get
from bs4 import BeautifulSoup as bSoup


# get the http response and store in a variable
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)

# find the all movie content
html_soup = bSoup(response.text, 'html.parser')
movie_containers = html_soup.findAll('div', class_='lister-item mode-advanced')

# grab the first movie
first_movie = movie_containers[0]

# extract first movie name
first_movie_name = first_movie.h3.a.text
print(first_movie_name)

# extract first movie name release year
first_movie_year = first_movie.find('span', class_='lister-item-year text-muted unbold').text
print(first_movie_year)

# extract first movie imdb rating
first_movie_imdb = float(first_movie.strong.text)
print(first_movie_imdb)

# extract first movie metacritic score
first_movie_mscore = first_movie.find('span', class_='metascore favorable')
first_movie_mscore = int(first_movie_mscore.text)
print(first_movie_mscore)

# extract first movie votes
first_movie_votes = first_movie.find('span', attrs={'name': 'nv'})
first_movie_votes = int(first_movie_votes['data-value'])
print(first_movie_votes)
