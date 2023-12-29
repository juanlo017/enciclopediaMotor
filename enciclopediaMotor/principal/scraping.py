from bs4 import BeautifulSoup
import requests

# SCRAPING FROM WEB:https://www.coches.net/nuevo/km-0/, 
# https://www.coches.net/nuevo/km-0/?pg=2 HASTA 
# https://www.coches.net/nuevo/km-0/?pg=289
import os, ssl


def get_pokemons():
    pokemon_list = []
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    soup = BeautifulSoup(requests.get('https://www.wikidex.net/wiki/Lista_de_Pokémon').text, "lxml")

    national_pokedexes = soup.find_all('table', class_='tabpokemon sortable mergetable')
    for pokedex in national_pokedexes:
        pokemon_rows = pokedex.find_all('tr')
        for pokemon_row in pokemon_rows:
            pokemon = pokemon_row.find_all('td')
            
            if len(pokemon) == 4:
                i = 1
            elif len(pokemon) == 3:
                i = 0
            else:
                continue

            pokemon_detail_url = f"https://www.wikidex.net/{pokemon[i].find('a')['href']}"
            pokemon_details = get_pokemon_details(pokemon_detail_url)
            pokemon_list.append(pokemon_details)
    return pokemon_list


def get_pokemon_details(url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    pokemon_details = soup.find('div', class_='cuadro_pokemon')

    name = pokemon_details.find('div', class_='titulo').text
    picture_url = pokemon_details.find('div', class_='vnav_datos').find('a', class_='image').attrs['href']
    complete_picture_url = f"https://www.wikidex.net/{picture_url}"
    number = pokemon_details.find('span', id='numeronacional').text
    
    tabla_datos = pokemon_details.find('table', class_='datos resalto')

    generation = tabla_datos.find('tr', title="Generación en la que apareció por primera vez").find('td').find('a').text

    types = tabla_datos.find('tr', title="Tipos a los que pertenece").find('td').find_all('a')
    list_types = []
    for type in types:
        title = type['title'] if type and 'title' in type.attrs else 'Title not found'
        list_types.append(title.replace('Tipo ', ''))

    weight = tabla_datos.find('tr', title="Peso del Pokémon").find('td').text
    weight = weight.replace('\n','')

    height =tabla_datos.find('tr', title="Altura del Pokémon").find('td').text
    height = height.replace('\n','')

    color = tabla_datos.find('tr', title="Color del Pokémon con el que se clasifica en la Pokédex").find('td').text
    color = color.split(' ')[0]

    description = soup.find('table', class_='pokedex radius10 tfx').find_all('tr')[1].find_all('td')
    description = ''.join(el.text for el in description).replace('\n','')

    pokemon = [name, number, generation, list_types, weight, height, color, description, complete_picture_url]
    return pokemon

def save_scrapped_data_to_file():
    pokemons = get_pokemons()
    print(pokemons)
    with open('pokemons.txt', 'w', encoding='utf-8') as f:
        for pokemon in pokemons:
            for att in pokemon:
                if type(att) is not list:
                    f.write(att + ';')
                else:
                    f.write(','.join(att) + ';')
            f.write('\n')
    return len(pokemons)
