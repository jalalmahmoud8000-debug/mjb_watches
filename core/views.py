from django.shortcuts import render
from products.models import Product


def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('-created_at')[:6]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:3]
    return render(request, 'core/home.html', {'featured_products': featured_products, 'latest_products': latest_products})


def about(request):
    """عرض صفحة من نحن"""
    return render(request, 'core/about.html')


def contact(request):
    """عرض صفحة اتصل بنا مع معالجة بسيطة للنموذج (عرض رسالة نجاح فقط)."""
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # هنا يمكن إضافة إرسال إيميل أو حفظ الرسالة في قاعدة البيانات.
        context['success'] = True
        context['name'] = name
    return render(request, 'core/contact.html', context)


def privacy(request):
    """صفحة سياسة الخصوصية"""
    return render(request, 'core/privacy.html')
