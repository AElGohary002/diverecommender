import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://dive.site'

def extract_continent(div_id):
    
    continent = div_id.rsplit('-', 1)[0]  # Split by the last hyphen 

    # Convert hyphens to spaces and capitalize each word
    continent = continent.replace('-', ' ').title()

    return continent



def scrape_countries():
    url = f'{BASE_URL}/destinations/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    country_links = []
    
    cont_div = soup.select('#all-destinations .destinations-list')

    for div in cont_div:

        div_id= div['id']
        continent = extract_continent(div_id)

        country_links.append(div_id)

        country_items = div.select('.destinations .title a')

        for country in country_items:
            country_name = country.text.strip()
            country_link = country['href']

            country_links.append({
                'continent': continent,
                'country': country_name,
                'link': country_link
            })
    return country_links

if __name__ == '__main__':
    print(scrape_countries())
