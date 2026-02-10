from django.shortcuts import render, redirect
from .models import Movie, Genre
from .forms import CreateMovieForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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


@login_required(login_url="/login/")
def movie_list(request):
    movies = Movie.objects.all()

    genre_id = request.GET.get("genre_id")
    if genre_id:
        movies = Movie.objects.filter(genre__id=genre_id)

    return render(request, "movies/movie_list.html", {"movies": movies})

@login_required(login_url="/login/")
def movie_create(request):
    if request.method == "GET":
        form = CreateMovieForm()
        genres = Genre.objects.all()
        return render(request, "movies/movie_create.html", {"form": form, "genres": genres})

    elif request.method == "POST":
        form = CreateMovieForm(request.POST, request.FILES)

        if form.is_valid():
            movie = Movie.objects.create(
                title=form.cleaned_data.get("title"),
                description=form.cleaned_data.get("description"),
                year=form.cleaned_data.get("year"),
                image=form.cleaned_data.get("image"),
            )

            movie.genre.set([form.cleaned_data.get("genre")])

            return redirect("/movies/")
        return HttpResponse("Error")
        



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