from django.shortcuts import render
from principal.populateDB import *
from principal.scraping import save_scrapped_data_to_file
from principal.forms import SearchTitleDescription, SearchByType


def home(request):
    return render(request, 'base.html')

def scrap_data(request):
    num_pokemons = save_scrapped_data_to_file()
    msg = 'Se han guardado ' + str(num_pokemons) + ' pokemons en el fichero pokemons.txt'
    return render(request, 'cargar.html',  {'msg':msg})

def load_db(request):
    num_pokemons = populate_DB()
    msg = 'Se han guardado ' + str(num_pokemons) + ' pokemons en la BBDD'
    return render(request, 'cargar.html', {'msg':msg})

def load_whoosh(request):
    num_pokemons = load_data_whoosh()
    msg = 'Se han guardado ' + str(num_pokemons) + ' pokemons en el Index de Whoosh'
    return render(request, 'cargar.html', {'msg':msg})

def search_whoosh_title_description(request):
    form = SearchTitleDescription()
    if request.method == 'POST':
        form = SearchTitleDescription(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                query = MultifieldParser(["name", "description"], ix.schema, group=OrGroup).parse(query)
                results = searcher.search(query, limit=None)
                print(results)
                msg = f'Se han encontrado {len(results)} resultados para la búsqueda: {query}'
                return render(request, 'search.html', {'results':results, 'msg':msg, 'form':form})
        else:
            print('no valido')
    return render(request, 'search.html', {'form':form})

def search_whoosh_type(request):
    form = SearchByType()
    pokemon_types = PokemonType.objects.values_list('name', flat=True)
    pokemon_types = [(name, name) for name in pokemon_types]
    form.fields['type'].choices = pokemon_types
    
    if request.method == 'POST':
        form = SearchByType(request.POST)
        form.fields['type'].choices = pokemon_types
        if form.is_valid():
            query = form.cleaned_data['type']
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                query = QueryParser("types", ix.schema).parse(query)
                results = searcher.search(query, limit=None)
                msg = f'Se han encontrado {len(results)} resultados para la búsqueda: {query}'
                return render(request, 'search.html', {'results':results, 'msg':msg, 'form':form})
        else:
            print('no valido')
    return render(request, 'search.html', {'form':form})

def search():
    pass