from django.shortcuts import render, redirect
from .models import Movie, Genre

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

    genre_id = request.GET.get("genre_id")
    if genre_id:
        movies = Movie.objects.filter(genre__id=genre_id)

    return render(request, "movies/movie_list.html", {"movies": movies})

def movie_create(request):
    if request.method == "GET":
        genres = Genre.objects.all()
        return render(request, "movies/movie_create.html", {"genres": genres})

    elif request.method == "POST":
        print(request.POST)
        title = request.POST.get("title")
        description = request.POST.get("description")
        year = request.POST.get("year")
        genre_id = request.POST.get("genre")
        image = request.FILES.get("image")

        movie = Movie.objects.create(title=title, description=description, year=year, image=image)

        movie.genre.set([genre_id])

        return redirect("/movies/")



def movie_detail(request, movie_id):
    if request.method == "GET":
        movie = Movie.objects.get(id=movie_id)
        return render(request, "movies/movie_detail.html", context={'movie': movie})

def home(request):
    if request.method == "GET":
        genres = Genre.objects.all()
        return render(request, "home.html", {"genres": genres})

def movies_by_genre(request, genre_id):
    if request.method == "GET":
        movies = Movie.objects.filter(genre__id=genre_id)
        return render(request, "movies/movie_list.html", {"movies": movies})