from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm
from products.models import Product, Category
from django.contrib.auth.decorators import login_required

# from cart.models import Cart, CartItem
from userspends.models import UserSpend, UserWinner
from spendations.models import Spend

# Create your views here.


def home_view(request):
    # p = timezone.now()
    products = Product.objects.filter(event=True, available=True)
    try:
        for product in products:
            product.save()
    except:
        pass
    category = Category.objects.all().order_by('-id')
    # latests = Product.objects.filter(ended=True).order_by('-updated')[:3]
    latests = UserWinner.objects.filter(
        product__ended=True).order_by('timestamp')[:3]
    return render(request, 'pages/home.html', {'products': products,
                                               'latests': latests,
                                               'category': category})


def contact_view(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        sender = form.cleaned_data['sender']  # username
        subject = form.cleaned_data['subject']  # email
        comment = form.cleaned_data['comment']
        if request.user.is_authenticated:
            subject = str(request.user)
        else:
            subject = 'کاربر ثبت نشده'

        comment = "این ایمیل از طرف: " + subject + f" ({first_name} {last_name})" + "\n با ایمیل:  " + sender + \
            " \n چنین پیامی را فرستاده:\n\n" + comment
        send_mail('DigiFood-user', comment, sender, [
                  'lordofhell225@gmail.com'], fail_silently=False)
        return redirect('pages:home-page')

    return render(request, 'pages/contact.html', {'form': form})
