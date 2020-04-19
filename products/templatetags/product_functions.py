from django import template
from products.models import ProductVotes
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def user_has_voted(username, product_id):    
    try:
        user = User.objects.get(username=username)
        user_vote = ProductVotes.objects.get(product__id=product_id, hunter=user)
        return True
    except ObjectDoesNotExist:
        return False