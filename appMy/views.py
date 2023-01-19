from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Q # ve veya işlemlerini kullanılmasına izin verir
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
    context={}
    card = Card.objects.get(id=id) # tek ürün istiyoruz
    comments = Comments.objects.filter(card = id)
    
    query = request.GET.get('q')
    if query:
        cards = Card.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
        return render(request,'allcard.html',{'cards':cards})
        
    if card.stok > 0:
        if request.method == "POST":
            if request.POST["button"] == "sepetbtn":
                adet = int(request.POST["adet"])
                if 1 <= adet <= 10:
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
    else:
        context.update({'hata':'Ürün Stokta kalmamıştır!'})     
    
    if request.method == "POST": 
        if request.POST["button"] == "commentbtn":
            name = request.POST["name"]
            email = request.POST["email"]
            comment = request.POST["comment"]
            
            comm = Comments(name=name, email=email, comment=comment,card=card )
            comm.save()
            return HttpResponseRedirect('/detay/{}/'.format(id))  # yönlendirme
        
        
    context.update({
        "card": card,
        "comments":comments,
    })
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
    toplam = 0
    for i in sepetler:
        toplam += i.price
        
    if request.method == "POST":
        adet = int(request.POST["adet"])
        product_id = request.POST["product-id"]
        if 1<= adet <= 10:
            product = Sepet.objects.filter(user=request.user).get(product = product_id)
            product.adet = adet
            product.price = adet * product.product.priece
            product.save()
            return redirect('sepetUser')        
    
    context = {
        "sepetler": sepetler,
        "toplam": toplam,
    }
    return render(request,'shoping.html', context)

def sepetDelete(request, id):
    product = Sepet.objects.get(id=id)
    product.delete()
    return redirect('sepetUser')

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
    logout(request)

    return redirect('loginUser')

def registerUser(request):
    
    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1==password2:
            user = User.objects.create_user(first_name = name, last_name=surname, email=email, username=username, password=password1)
            user.save()
            
            return redirect('loginUser')
    
    context={
        
    }
    return render(request, 'users/register.html',context)
