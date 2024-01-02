from principal.models import PokemonType, Pokemon
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, NUMERIC, ID
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
import os, shutil

def populate_DB():
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
                                        description=pokemon_att[7],
                                        picture_url=pokemon_att[8]
                                    )[0]
            pokemon.types.set(pokemon_types)
            pokemon.save()
            pokemon_counter += 1
    return pokemon_counter

def load_data_whoosh():
    schem = Schema(name=TEXT(stored=True), 
                   number=NUMERIC(stored=True), 
                   generation=KEYWORD(stored=True), 
                   weight=NUMERIC(stored=True, numtype=float), 
                   height=NUMERIC(stored=True, numtype=float), 
                   color=TEXT(stored=True), 
                   description=TEXT(stored=True), 
                   picture_url=ID(stored=True),
                   types=KEYWORD(stored=True,commas=True,lowercase=True))
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        writer.add_document(name=pokemon.name, 
                            number=pokemon.number, 
                            generation=pokemon.generation, 
                            weight=pokemon.weight, 
                            height=pokemon.height, 
                            color=pokemon.color, 
                            description=pokemon.description, 
                            picture_url=pokemon.picture_url,
                            types=','.join([type.name for type in pokemon.types.all()]))
    writer.commit()
    return len(pokemons)

def search_whoosh_type(input):
    ix = open_dir("Index")
    with ix.searcher() as searcher:
        query = QueryParser("types", ix.schema).parse(input)
        results = searcher.search(input)
        return results

def search_whoosh_range_number(query1, query2, field='number'):
    ix = open_dir("Index")
    with ix.searcher() as searcher:
        query = QueryParser(field, ix.schema).parse(u"["+query1+" TO "+query2+"]")
        results = searcher.search(query)
        return results
