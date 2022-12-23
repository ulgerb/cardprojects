from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Q # ve veya işlemlerini kullanılmasına izin verir
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    cards = Card.objects.all()
    kategoriler = Category.objects.all()
    
    query = request.GET.get('q')
    if query:
        cards = Card.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    
    
    
    context={   
        "cards":cards,
        "kategoriler": kategoriler,
    }
    return render(request,'index.html',context)

def Detail(request,id):
    card = Card.objects.get(id=id) # tek ürün istiyoruz
    comments = Comments.objects.filter(card = id)
    
    query = request.GET.get('q')
    if query:
        cards = Card.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
        return render(request,'allcard.html',{'cards':cards})
        
    
    if request.method == "POST": 
        name = request.POST["name"]
        email = request.POST["email"]
        comment = request.POST["comment"]
        
        comm = Comments(name=name, email=email, comment=comment,card=card )
        comm.save()
        return HttpResponseRedirect('/detay/{}/'.format(id))  # yönlendirme
        
        
    context={
        "card": card,
        "comments":comments,
    }
    return render(request,'detail.html',context)

def allCard(request,id="all"):
    
    cards = Card.objects.all()
    kategoriler = Category.objects.all()

    query = request.GET.get('q')
    if query:
        cards = Card.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))

    if id.isnumeric():
        cards = Card.objects.filter(category=id)
    
    # Paginator
    paginator = Paginator(cards, 2)
    page_number = request.GET.get('page')
    cards = paginator.get_page(page_number)
    
    context = {
        "cards": cards,
        "kategoriler": kategoriler,
    }
    return render(request, 'allcard.html', context)

