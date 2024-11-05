import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://dive.site'

def extract_continent(div_id):
    
    continent = div_id.rsplit('-', 1)[0]  # Split by the last hyphen 

    # Convert hyphens to spaces and capitalize each word
    continent = continent.replace('-', ' ').title()

    return continent


def extract_dive_types(country_link):
    response = requests.get(country_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    dive_types = []
    dive_type_div = soup.select('.info .diving-types span')

    for div in dive_type_div:
        dive_types.append(div.text.strip())

    return dive_types

def extract_logged_species(country_link):
    response = requests.get(country_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    logged_species = None
    
    logged_species_div = soup.select('.col-md-16 .block.counter-text')
    for div in logged_species_div:
        label = div.select_one('.small.text-uppercase.block.font-weight-light')
        if label and 'Logged Species' in label.text:
            count_span = div.select_one('.count')
            if count_span:
                logged_species = int(count_span.text.strip())
            break

    return logged_species

def scrape_data():
    url = f'{BASE_URL}/destinations/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    country_links = []
    
    cont_div = soup.select('#all-destinations .destinations-list')

    for div in cont_div:

        div_id= div['id']

        continent = extract_continent(div_id)

        country_items = div.select('.destinations .title a')

        for country in country_items:
            country_name = country.text.strip()
            country_link = country['href']

            # Get dive types
            dive_types = extract_dive_types(country_link)
            # Get logged species
            logged_species = extract_logged_species(country_link)

            country_links.append({
                'continent':continent,
                'country':country_name,
                'link':country_link,
                'Dive Types': dive_types,
                'Logged Species': logged_species
            })
    return country_links


if __name__ == '__main__':
    print(scrape_data())

# TO BE ADDED ITEMS

    # def scrape_dive_details(country_link):
#     response = requests.get(country_link)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     dive_details = {
#         'General Info': extract_content(soup, 'general-info'),
#         'Diving Info': extract_content(soup, 'diving-info')
#     }


#     # general_info_header = soup.find('h1', id='general-info')
#     # if general_info_header:
#     #     content = general_info_header.find_next_sibling('div', class_ = 'info-text')
#     #     if content:
#     #         dive_details['General Info'] = content.text.strip()
    
#     # # dive_season = TO BE ADDED

#     return dive_details

"""
def extract_weather_conditions(country_link):
    response = requests.get(country_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    weather_highC = None
    weather_lowC = None
"""