from django.shortcuts import render
from principal.populateDB import populate_DB, almacenar_datos_whoosh
from principal.scraping import save_scrapped_data_to_file


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
    num_pokemons = almacenar_datos_whoosh()
    msg = 'Se han guardado ' + str(num_pokemons) + ' pokemons en el Index de Whoosh'
    return render(request, 'cargar.html', {'msg':msg})





