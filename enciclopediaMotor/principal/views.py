from django.shortcuts import render
from principal.populateDB import populate_DB
from principal.scraping import save_scrapped_data_to_file

# Create your views here.
def scrapear(request):
    num_pokemons = save_scrapped_data_to_file()
    return render(request, 'scrapear.html',  {'num_pokemons':num_pokemons})

def cargar(request):
    num_pokemons = populate_DB()
    return render(request, 'cargar.html', {'num_pokemons':num_pokemons})

def home(request):
    return render(request, 'base.html')

