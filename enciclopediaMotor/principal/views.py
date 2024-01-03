from django.shortcuts import render
from principal.populateDB import *
from principal.scraping import save_scrapped_data_to_file
from principal.forms import SearchTitleDescription, SearchByType, SearchRange, SearchRangeFloat


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

def search_whoosh_range(request):
    form = SearchRange()
    if request.method == 'POST':
        form = SearchRange(request.POST)
        if form.is_valid():
            query1 = form.cleaned_data['min']
            query2 = form.cleaned_data['max']
            field = form.cleaned_data['field']
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                rng = '['+str(query1)+' TO '+str(query2)+']'
                query = QueryParser(field, ix.schema).parse(rng)
                results = searcher.search(query, limit=None)
                msg = f'Se han encontrado {len(results)} resultados para la búsqueda en rango: {query1} - {query2}'
                return render(request, 'search.html', {'results':results, 'msg':msg, 'form':form})
        else:
            print('no valido')
    return render(request, 'search.html', {'form':form})

def search_whoosh_range_float(request):
    form = SearchRangeFloat()
    if request.method == 'POST':
        form = SearchRangeFloat(request.POST)
        if form.is_valid():
            query1 = form.cleaned_data['min']
            query2 = form.cleaned_data['max']
            field = form.cleaned_data['field']
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                rng = '['+str(query1)+' TO '+str(query2)+']'
                query = QueryParser(field, ix.schema).parse(rng)
                results = searcher.search(query, limit=None)
                msg = f'Se han encontrado {len(results)} resultados para la búsqueda en rango: {query1} - {query2}'
                return render(request, 'search.html', {'results':results, 'msg':msg, 'form':form})
        else:
            print('no valido')
    return render(request, 'search.html', {'form':form})





