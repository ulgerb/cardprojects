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
    comments = Comments.objects.filter(card = id)
    
    if request.method == "POST": 
        name = request.POST["name"]
        email = request.POST["email"]
        comment = request.POST["comment"]
        
        comm = Comments(name=name, email=email, comment=comment,card=card )
        comm.save()
        
    context={
        "card": card,
        "comments":comments,
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

