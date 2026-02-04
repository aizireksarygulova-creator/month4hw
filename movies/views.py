from django.shortcuts import render
from .models import Movie

# select * from product;
# Product.objects.all()

# select * from product where id= '2';
# Product.objects.get(id=2) ==  возвращает 1 обьект

# select * from product where name = 'laptop';
# Product.objects.filter(name='laptop')

# select * from product $LIKE where name = 'laptop' and price = '1000';
# Product.objects.filter(name_icontains='laptop', price=1000)

# Product.objects.update(price=1000) == изменение всех продуктов

# Product.objects.create(name='laptop', price=10, description='laptop')

# Product.objects.delete()



def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', context={'movies': movies})


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, "movies/movie_detail.html", context={'movie': movie})

def home(request):
    return render(request, "home.html")