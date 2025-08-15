from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
    your_last= forms.CharField(label='your_last', max_length=20)
    your_lat= forms.CharField(label='your_last', widget=forms.Textarea)
