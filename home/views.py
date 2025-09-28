from django.shortcuts import render

def index(request):
    template_data = {"title": "Food Fairy"}
    return render(request, 'home/index.html', {"template_data": template_data})

def about_page(request): 
    template_data = {"title": "About"}
    return render(request, 'home/about.html', {"template_data": template_data})