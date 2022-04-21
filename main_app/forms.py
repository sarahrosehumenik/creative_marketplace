from django.forms import ModelForm, ChoiceField
from .models import Comment, Product, Tag
 
class CommentForm(ModelForm):
 class Meta:
   model = Comment
   fields = ['text']

class SearchForm(ModelForm):
  class Meta:
    model = Product
    fields = ['tags']
  def __init__(self, **kwargs):
    super(SearchForm, self).__init__(**kwargs)
    self.fields['tags'].required = False
   


