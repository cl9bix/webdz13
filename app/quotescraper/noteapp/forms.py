from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelMultipleChoiceField, SelectMultiple, ModelChoiceField, Select
from .models import Author, Quote, Tag


class RegisterAuthor(ModelForm):
    fullname = CharField(max_length=100,
                         required=True,
                         widget=TextInput(attrs={'class': 'form-control'}))

    born_date = DateField(widget=DateInput(attrs={'class': 'form-control'}))

    born_location = CharField(max_length=150,
                              required=True,
                              widget=TextInput(attrs={'class': 'form-control'}))

    description = CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class RegisterQuote(ModelForm):
    quote = CharField(required=True,
                      widget=TextInput(attrs={'class': 'form-control'}))

    tags = ModelChoiceField(queryset=Tag.objects.all().order_by('name'), empty_label="(Nothing)",
                                    widget=Select(attrs={"class": "form-select"}))

    author = ModelChoiceField(queryset=Author.objects.all().order_by('fullname'), empty_label="(Nothing)",
                              widget=Select(attrs={"class": "form-select"}))

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']

    def __init__(self, *args, **kwargs):
        super(RegisterQuote, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all().order_by('name')
        self.fields['tags'].label_from_instance = lambda obj: obj.name
        self.fields['author'].queryset = Author.objects.all().order_by('fullname')
        self.fields['author'].label_from_instance = lambda obj: obj.fullname


class RegisterTag(ModelForm):
    name = CharField(min_length=3,
                     max_length=50,
                     required=True,
                     widget=TextInput(attrs={"class": "form-control"}))

    def __str__(self):
        return self.name

    class Meta:
        model = Tag
        fields = ['name']


