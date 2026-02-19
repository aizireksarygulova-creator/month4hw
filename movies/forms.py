from django import forms
from .models import Genre

spisok_bad_words = ["ismar", "казино", "aizirek"]


class CreateMovieForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    year = forms.IntegerField()
    image = forms.ImageField(required=False)

    
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        if title in spisok_bad_words:
            raise forms.ValidationError("Это слово запрещено")
        return data


YEAR_CHOICES = (
    ("", "Любой год"),
    ("2026", "2026"),
    ("2025", "2025"),
    ("2024", "2024"),
    ("2020_2023", "2020-2023"),
)

class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Поиск фильма..."
        })
    )

    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label="Жанры",
        widget=forms.CheckboxSelectMultiple
    )

    year_choice = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        label="",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )