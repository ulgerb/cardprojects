from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    cards = Card.objects.all()
    kategoriler = Category.objects.all()
    
    context={   
        "cards":cards,
        "kategoriler": kategoriler,
    }
    return render(request,'index.html',context)

def Detail(request,id):
    card = Card.objects.get(id=id) # tek ürün istiyoruz
    
    
    if request.method == "POST": 
        print(request.POST)
        
        
    context={
        "card": card,
    }
    return render(request,'detail.html',context)

def allCard(request,id="all"):
    
    cards = Card.objects.all()
    kategoriler = Category.objects.all()

    if id.isnumeric():
        cards = Card.objects.filter(category=id)
    
    context = {
        "cards": cards,
        "kategoriler": kategoriler,
    }
    return render(request, 'allcard.html', context)

