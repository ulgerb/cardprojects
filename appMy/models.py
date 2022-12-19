from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(("Kategori Adı"), max_length=50) 
    
    def __str__(self):
        return self.name

class Card(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category, verbose_name=("Kategori"), on_delete=models.CASCADE, null=True)
    title = models.CharField(("Başlık"), max_length=50)
    text = models.TextField(("Card yazısı"))
    priece = models.IntegerField(("Fiyat"), null=True)
    image = models.FileField(("Card Resim"), upload_to='', max_length=100)
    date_now = models.DateTimeField(("Paylaşım Zamanı"), auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Comments(models.Model):
    name = models.CharField(("Ad Soyad"), max_length=80)
    email = models.EmailField(("Email"), max_length=254)
    comment = models.TextField(("Yorum"), max_length=500)

    def __str__(self):
        return self.title
