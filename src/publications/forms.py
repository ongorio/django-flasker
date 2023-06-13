from django import forms

from publications.models import Publication, Comment

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)