from django.shortcuts import render
from .models import DiveDestination

def filter_destination(request):

    continents = DiveDestination.objects.values_list('continent', flat=True).distinct()

    all_dive_types_combinations = DiveDestination.objects.values_list('dive_types', flat=True).distinct()
    dive_types = set()
    
    for combination in all_dive_types_combinations:
        if combination:
            types = combination.split(', ')
            dive_types.update(types)

    destinations = DiveDestination.objects.all()

    selected_continent = request.GET.get('continent')
    selected_dive_type = request.GET.get('dive_type')
    min_logged_species = request.GET.get('min_logged_species')

    if selected_continent:
        destinations = destinations.filter(continent = selected_continent)

    if selected_dive_type:
        destinations = destinations.filter(dive_types__icontains = selected_dive_type)

    if min_logged_species:
        destinations = destinations.filter(logged_species__gte = min_logged_species)

    context = {
        'continents': continents,
        'destinations': destinations,
        'dive_types': sorted(dive_types),
        'selected_continent': selected_continent,
        'selected_dive_type': selected_dive_type,
        'min_logged_species': min_logged_species,
    }
    return render(request, 'divesite_recommender_app/filter_destination.html', context)