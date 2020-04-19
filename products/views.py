from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, ProductVotes


def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products': products})

@login_required(login_url="/accounts/login")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'All * fields are required'})    
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})

@login_required(login_url="/accounts/login")
def upvote(request, product_id):
    product = get_object_or_404(Product, pk=product_id)        
    try:
        user_vote = ProductVotes.objects.get(product=product, hunter=request.user)
        return redirect(request.POST.get('previous_url', '/'))
    except ObjectDoesNotExist:
        user_vote = ProductVotes()
        user_vote.hunter = request.user
        user_vote.product = product
        user_vote.save()    
        return redirect(request.POST.get('previous_url', '/'))

@login_required(login_url="/accounts/login")
def downvote(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        user_vote = ProductVotes.objects.get(product=product, hunter=request.user)
        user_vote.delete()
        return redirect(request.POST.get('previous_url', '/'))
    except ObjectDoesNotExist:
        return redirect(request.POST.get('previous_url', '/'))