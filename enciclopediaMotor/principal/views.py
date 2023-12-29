from django.shortcuts import render
from principal.scraping import get_pokemons


# Create your views here.
def cargar(request):
    pokemon_list = get_pokemons()
    return render(request, 'cargar.html', {'pokemon_list':pokemon_list})

def home(request):
    return render(request, 'base.html')

