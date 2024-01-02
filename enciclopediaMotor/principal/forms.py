from django import forms

class SearchTitleDescription(forms.Form):
    query = forms.CharField(label='Buscar', widget=forms.TextInput, required=True)

class SearchByType(forms.Form):
    type = forms.ChoiceField(label='Tipo', required=True, choices=[])