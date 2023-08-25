from django import template
from ..utils import get_mongodb

register = template.Library()


def get_author(fullname):
    db = get_mongodb()
    author = db.authors.find_one({'_id': fullname})
    return author['fullname']


register.filter('author', get_author)
