from django.shortcuts import render
from django.db.models import Q
from .models import Product, Brand, Category


def product_list(request):
    qs = Product.objects.filter(is_active=True)

    # filters from GET
    q = request.GET.get('q')
    brand = request.GET.get('brand')
    category = request.GET.get('category')
    gender = request.GET.get('gender')
    featured = request.GET.get('featured')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if brand:
        qs = qs.filter(brand__id=brand)

    if category:
        qs = qs.filter(categories__id=category)

    if gender in ['M', 'F', 'U']:
        qs = qs.filter(gender=gender)

    if featured == '1':
        qs = qs.filter(is_featured=True)

    qs = qs.order_by('-is_featured', '-created_at').distinct()

    brands = Brand.objects.all()
    categories = Category.objects.all()

    context = {
        'products': qs,
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'products/list.html', context)


def category_list(request):
    from .models import Category
    cats = Category.objects.all()
    return render(request, 'products/categories.html', {'categories': cats})


def category_detail(request, slug):
    from .models import Category
    cat = Category.objects.filter(slug=slug).first()
    if not cat:
        return render(request, 'products/list.html', {'products': Product.objects.none()})
    qs = cat.products.filter(is_active=True).order_by('-is_featured', '-created_at')
    return render(request, 'products/list.html', {'products': qs, 'current_category': cat})


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug, is_active=True).first()
    if not product:
        # could return 404, but keep simple
        return render(request, 'products/detail.html', {'product': None})
    return render(request, 'products/detail.html', {'product': product})
