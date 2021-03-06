import re
from random import randint

from django.db.models import Q, Max
from django.shortcuts import render

from .forms import MineralSearchForm
from .models import Mineral


def detail(request, pk):
    """View that accepts a mineral pk and displays the details of that
    particular mineral. Returns 404 if mineral doesn't exist.
    """
    mineral = Mineral.objects.get(id=pk)
    fields = mineral.fields_lower
    context = {
        'mineral': mineral,
        'form': MineralSearchForm(),
        'fields': fields,
    }
    return render(request, 'mineralsearchapp/detail.html', context)


def random(request):
    """View that returns a random mineral and its details
    """
    minerals = Mineral.objects.aggregate(
        number_of_minerals=Max('id')
    )
    number = minerals['number_of_minerals']
    mineral = Mineral.objects.get(
        id=randint(1, number)
    )
    fields = mineral.fields_lower
    context = {
        'mineral': mineral,
        'form': MineralSearchForm(),
        'fields': fields,
    }
    return render(request, 'mineralsearchapp/detail.html', context)


def letter(request, letter='a'):
    """View that takes in a letter kwarg and finds all minerals that
    start with that character
    """
    minerals = Mineral.objects.values(
        'name',
        'pk'
    ).filter(
        name__startswith=letter
    ).order_by(
        'name'
    )
    form = MineralSearchForm()
    context = {
        'minerals': minerals, 
        'form': form,  
        'alphaquery': letter,    
    }
    return render(request, 'mineralsearchapp/index.html', context)


def search(request):
    """View that accepts q query from the MineralSearchForm and filters
    mineral names on that query
    """
    form = MineralSearchForm()
    if request.method == 'GET':
        form = MineralSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['q']
            minerals = Mineral.objects.values(
                'name',
                'pk'
            ).filter(
                Q(name__icontains=query) |
                Q(image_caption__icontains=query) |
                Q(category__icontains=query) |
                Q(formula__icontains=query) |
                Q(strunz_classification__icontains=query) |
                Q(crystal_system__icontains=query) |
                Q(unit_cell__icontains=query) |
                Q(color__icontains=query) |
                Q(crystal_symmetry__icontains=query) |
                Q(cleavage__icontains=query) |
                Q(mohs_scale_hardness__icontains=query) |
                Q(luster__icontains=query) |
                Q(streak__icontains=query) |
                Q(diaphaneity__icontains=query) |
                Q(group__icontains=query) |
                Q(optical_properties__icontains=query) |
                Q(refractive_index__icontains=query) |
                Q(crystal_habit__icontains=query) |
                Q(specific_gravity__icontains=query)
            ).order_by(
                'name'
            )
            context = {
                'minerals': minerals,
                'form': form,
            }
            return render(request, 'mineralsearchapp/index.html', context)
    minerals = Mineral.objects.values(
        'name',
        'pk'
    ).order_by(
        'name'
    )
    context = {
            'minerals': minerals,
            'form': form,
        }
    return render(request, 'mineralsearchapp/index.html', context)


def group(request, group):
    """View that accepts a group query and returns a queryset of 
    minerals filtered on the group field
    """
    minerals = Mineral.objects.values(
        'name',
        'pk'
    ).filter(
        group__icontains=group
    )
    context = {
        'minerals': minerals,
        'form': MineralSearchForm(),
        'groupquery': group,
    }
    return render(request, 'mineralsearchapp/index.html', context)


def colour(request, colour):
    """View that accepts a colour query and returns a queryset of 
    minerals filtered on the colour field
    """
    minerals = Mineral.objects.values(
        'name',
        'pk'
    ).filter(
        color__icontains=colour
    )
    context = {
        'minerals': minerals,
        'form': MineralSearchForm(),
        'colourquery': colour,
    }
    return render(request, 'mineralsearchapp/index.html', context)
    