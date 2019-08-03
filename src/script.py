from requests import get
from bs4 import BeautifulSoup as bSoup
from time import time
from time import sleep
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import csv

pages = [str(i) for i in range(1, 5)]
years_url = [str(i) for i in range(2002, 2020)]
headers = {"Accept-Language": "en-US, en;q=0.5"}

# Preparing the monitoring for the loop
start_time = time()
requests = 0

# Create a CSV file for storing all the date
csv_file = open('movie_rating.csv', 'w')
csv_writer = csv.writer(csv_file)
headers_row = ['movie_name', 'release_year', 'imdb', 'metascore', 'votes']
csv_writer.writerow(headers_row)

# For every year in the interval 2000-2019
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:
        response = get('http://www.imdb.com/search/title?release_date=' + year_url + '&sort=num_votes,desc&page=' + page, headers=headers)

        # Pause the loop
        sleep(randint(8, 15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print(f'Request: {requests} Frequency: {requests/elapsed_time} requests/s')
        clear_output(wait=True)

        # Throw a warning for non-200 status code
        if response.status_code != 200:
            warn(f'Request: {requests}; Status code: {response.status_code}')

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of requests with BeautifulSoup
        page_html = bSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.findAll('div', class_='lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_='ratings-metascore') is not None:
                # Scrape the name
                name = container.h3.a.text

                # Scrape the year
                year = container.h3.find('span', class_='lister-item-year').text

                # Scrape the IMDB rating
                imdb = float(container.strong.text)

                # Scrape the Metascore
                m_score = container.find('span', class_='metascore').text

                # Scrape the number of votes
                votes = container.find('span', attrs={'name': 'nv'})['data-value']

                # Write each movie details into csv files
                movie_row = [name, year, imdb, m_score, votes]
                csv_writer.writerow(movie_row)

# Now close the CSV file
csv_file.close()
