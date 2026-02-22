from django.shortcuts import render, redirect
from .models import Movie, Genre
from .forms import CreateMovieForm, SearchForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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

# Product.objects.all() -> products = [product1, product2, product3, product4, product5, product6, product7, product8, product9, product10]
# limit = 3
# page = 1
# product = products[(page-1)*limit:page*limit]
# max_page = int(len(products)/limit)
# срезы = [start:stop]
#
# FBV -> Function Based View
# CBV -> Class Based View


@login_required(login_url="/login/")
def movie_list(request):

    movies = Movie.objects.all()
    genres = Genre.objects.all()

    search_query = request.GET.get("search", "")
    selected_genres = request.GET.getlist("genre_id")
    selected_genres = [g for g in selected_genres if g]
    year_choice = request.GET.get("year_choice")


    
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    
    if selected_genres:
        movies = movies.filter(genre__id__in=selected_genres).distinct()

    
    if year_choice:
        if year_choice == "2026":
            movies = movies.filter(year=2026)
        elif year_choice == "2025":
            movies = movies.filter(year=2025)
        elif year_choice == "2024":
            movies = movies.filter(year=2024)
        elif year_choice == "2020_2023":
            movies = movies.filter(year__gte=2020, year__lte=2023)

    limit = 4

    page = int(request.GET.get("page")) if request.GET.get("page") else 1

    total_movies = len(movies)

    max_page = total_movies // limit
    if total_movies % limit != 0:
        max_page += 1

    start = (page - 1) * limit
    stop = page * limit

    list_pages = range(1, max_page + 1)

    movies = movies[start:stop]
    return render(
        request,
        "movies/movie_list.html",
        {
            "movies": movies,
            "genres": genres,
            "selected_genres": selected_genres,
            "selected_year": year_choice,
            "search_value": search_query,
            "list_pages": list_pages,
        }
    )

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
                    profile = request.user.profile,
                    title=form.cleaned_data.get("title"),
                    description=form.cleaned_data.get("description"),
                    year=form.cleaned_data.get("year"),
                    image=form.cleaned_data.get("image"),
                )

            
                movie.genre.set(form.cleaned_data.get("genre"))

                return redirect("/movies/")
        return HttpResponse("Error")

def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.user.profile != movie.profile:
        return HttpResponse("Permission denied")
    movie.delete()
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