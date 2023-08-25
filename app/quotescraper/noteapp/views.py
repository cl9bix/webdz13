from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .utils import get_mongodb
from .models import Tag, Author, Quote
from .forms import RegisterAuthor, RegisterQuote, RegisterTag


popular_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
popular_tags = [(tag, 2.75 * tag.num_quotes) for tag in popular_tags]


def main(request, page=1):
    context = {}
    # db = get_mongodb()
    # quotes = db.quotes.find()
    quotes = Quote.objects.all()

    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    context['popular_tags'] = popular_tags
    context['quotes'] = quotes_on_page
    return render(request, 'quotes/index.html', context=context)


def author_detail(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, 'quotes/author.html', context={'author': author})


def selected_tag(request, tag_name, page=1):
    tag = Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'quotes': quotes,
        'popular_tags': popular_tags,
    }
    return render(request, 'quotes/tags.html', context=context)


@login_required
def add_author(request):
    if request.method == 'POST':
        form = RegisterAuthor(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author.html', context={'form': form})

    return render(request, 'quotes/add_author.html', context={'form': RegisterAuthor()})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = RegisterQuote(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', context={'form': form})

    return render(request, 'quotes/add_quote.html', context={'form': RegisterQuote()})

