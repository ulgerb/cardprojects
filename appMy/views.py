from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Q # ve veya işlemlerini kullanılmasına izin verir
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    cards = Card.objects.all().order_by("?")[:3] # order_by sıralama, [:3] parçalama
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
        if request.POST["button"] == "sepetbtn":
            adet = int(request.POST["adet"])
            if Sepet.objects.filter(user=request.user, product=card).exists():
                sepet = Sepet.objects.filter(user=request.user).get(product=card)
                sepet.adet += adet 
                sepet.price += adet * card.priece
                sepet.save()
                return redirect('index')
            else:
                price = adet * card.priece
                sepet = Sepet(user = request.user, product=card, adet=adet, price=price)
                sepet.save()
                return redirect('index')
            
    
    if request.method == "POST": 
        if request.POST["button"] == "commentbtn":
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

def sepetUser(request):
    sepetler = Sepet.objects.filter(user=request.user)
    
    context = {
        "sepetler": sepetler
    }
    return render(request,'shoping.html', context)

# USER
def loginUser(request):
    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect("index")
    
    return render(request,'users/login.html',context)


def logoutUser(request):
    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")

    return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)

    return redirect('loginUser')