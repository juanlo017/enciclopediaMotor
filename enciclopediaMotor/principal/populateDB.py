import re
from principal.scraping import get_pokemons
from principal.models import PokemonType, Pokemon

def populate_DB():
    #delete all data from DB
    PokemonType.objects.all().delete()
    Pokemon.objects.all().delete()

    pokemon_counter = 0
    with open('./pokemons.txt', 'r', encoding='utf-8') as file:
        for line in file:
            pokemon_att = line.split(';')

            pokemon_types = []
            for type in pokemon_att[3].split(','):
                pokemon_type = PokemonType.objects.get_or_create(name=type)[0]
                pokemon_type.save()
                pokemon_types.append(pokemon_type)

            weight_to_float =float(pokemon_att[4].split(' ')[0].replace(',','.'))
            height_to_float =float(pokemon_att[5].split(' ')[0].replace(',','.'))

            pokemon = Pokemon.objects.get_or_create(
                                        name=pokemon_att[0], 
                                        number=pokemon_att[1], 
                                        generation=pokemon_att[2], 
                                        weight=weight_to_float, 
                                        height=height_to_float, 
                                        color=pokemon_att[6], 
                                        picture_url=pokemon_att[7]
                                    )[0]
            
            pokemon.types.set(pokemon_types)
            pokemon.save()
            pokemon_counter += 1
    return pokemon_counter