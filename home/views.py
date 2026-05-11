from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .form import MyForm
from home.models import topslider, Welcometext, Welcomelist, Services, Call, OurAnimals, Offers, Contact, Customer, \
    MembershipCardOrder, MembershipOrder, Address, Email
from django.contrib.auth import authenticate, login, logout
from home.models import UserCreateFrom

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Services, OurAnimals, topslider, Welcometext, Welcomelist, Offers, Contact, Address, Email
from .serializers import (ServicesSerializer, AnimalSerializer, SliderSerializer, 
                          WelcomeTextSerializer, WelcomeListSerializer, OffersSerializer, 
                          ContactSerializer, AddressSerializer, EmailSerializer)

# Create your views here.


def home(request):
    slider = topslider.objects.all()
    wtext = Welcometext.objects.first()
    wlist = Welcomelist.objects.all()
    service = Services.objects.all()
    call = Call.objects.first()
    address = Address.objects.first()
    animal = OurAnimals.objects.all()
    offers = Offers.objects.all()
    email = Email.objects.first()
    context = {
        'slider': slider,
        'wtext': wtext,
        'wlist': wlist,
        'service': service,
        'call': call,
        'animal': animal,
        'offers': offers,
        'address': address,
        'email': email,

    }
    return render(request, 'index.html', context)


def about(request):
    wtext = Welcometext.objects.first()
    wlist = Welcomelist.objects.all()

    context = {
        'wtext': wtext,
        'wlist': wlist,

    }
    return render(request, 'about.html', context)


def services(request):
    service = Services.objects.all()
    call = Call.objects.first()
    context = {
        'service': service,
        'call': call,
    }

    return render(request, 'service.html', context)


def animals(request):
    animal = OurAnimals.objects.all()
    context = {
        'animal': animal,
    }
    return render(request, 'animal.html', context)


def membership(request):
    offers = Offers.objects.all()
    context = {'offers': offers}
    return render(request, 'membership.html', context)


def order_membership(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        offer = Offers.objects.get(pk=offer_id)

        user_email = request.POST.get('user_email')
        user_name = request.POST.get('user_name')

        order = MembershipOrder.objects.create(
            offer=offer,
            user_email=user_email,
            user_name=user_name
        )

        return redirect('order_success')

    return redirect('membership')
def visting(request):
    return render(request, 'visiting.html')


def testmonial(request):
    return render(request, 'testimonial.html')


def contact(request):
    call = Call.objects.first()
    address = Address.objects.first()
    email = Email.objects.first()

    context = {
        'call': call,
        'address': address,
        'email': email,
    }

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        cont = Contact(name=name, email=email, subject=subject, message=message)
        cont.save()
    return render(request, 'contact.html', context)
@login_required(login_url="/accounts/login/")
def form(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Process the form data
            first = form.cleaned_data['first']
            last = form.cleaned_data['last']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '')  # Use get() to avoid KeyError
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip']
            adult = form.cleaned_data['adult']
            kids = form.cleaned_data['kids']

            # Save form submission to the database
            submission = Customer.objects.create(
                first=first,
                last=last,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zip=zip_code,
                adult=adult,
                kids=kids
            )

            # Sending email
            subject = 'Form Submission'
            message = f'''
            Name: {first} {last}
            Email: {email}
            Phone: {phone}
            Address: {address}, {city}, {state} {zip_code}
            Adults: {adult}
            Kids: {kids}
            '''
            send_mail(subject, message, 'your_email@example.com', [email])

            # Optionally, you can redirect the user to a thank you page
            return render(request, 'thank_you.html', {'first': first})
    else:
        form = MyForm()

    return render(request, 'Form.html', {'form': form})
def thankyou(request):
    return render(request, 'thank_you.html')

# registration
def signup(request):
    if request.method == 'POST':
        form = UserCreateFrom(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('form')
    else:
        form = UserCreateFrom()
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html',context)


def custom_logout(request):
    logout(request)
    # Redirect to a desired page after logout
    return redirect('login')


@api_view(['GET'])
def get_all_data_api(request):
    data = {
        "sliders": topslider.objects.all(),
        "welcome_text": Welcometext.objects.all(),
        "welcome_list": Welcomelist.objects.all(),
        "services": Services.objects.all(),
        "animals": OurAnimals.objects.all(),
        "offers": Offers.objects.all(),
        "address": Address.objects.all(),
        "email": Email.objects.all(),
    }
    return Response({
        "status": "Success",
        "sliders": SliderSerializer(data["sliders"], many=True).data,
        "welcome": {
            "text": WelcomeTextSerializer(data["welcome_text"], many=True).data,
            "list": WelcomeListSerializer(data["welcome_list"], many=True).data,
        },
        "services": ServicesSerializer(data["services"], many=True).data,
        "animals": AnimalSerializer(data["animals"], many=True).data,
        "offers": OffersSerializer(data["offers"], many=True).data,
        "contact_info": {
            "address": AddressSerializer(data["address"], many=True).data,
            "email": EmailSerializer(data["email"], many=True).data,
        }
    })





