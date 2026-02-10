from django import forms

spisok_bad_words = ["ismar", "казино", "aizirek"]


class CreateMovieForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    year = forms.IntegerField()
    image = forms.ImageField()
    genre = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        if title in spisok_bad_words:
            raise forms.ValidationError("Это слово запрещено")
        return data
    


