from django import forms

class SearchTitleDescription(forms.Form):
    query = forms.CharField(label='Buscar', widget=forms.TextInput, required=True)

class SearchByType(forms.Form):
    type = forms.ChoiceField(label='Tipo', required=True, choices=[])

class SearchRange(forms.Form):
    min = forms.IntegerField(label='Min', required=True)
    max = forms.IntegerField(label='Max', required=True)
    field = forms.ChoiceField(label='Campo', required=True, choices=[('number', 'number')])


class SearchRangeFloat(forms.Form):
    min = forms.FloatField(label='Min', required=True)
    max = forms.FloatField(label='Max', required=True)
    field = forms.ChoiceField(label='Campo', required=True, choices=[('weight', 'weight'), ('height', 'height')])