from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .form import MyForm
from home.models import Topslider, Welcometext, Welcomelist, Services, Call, OurAnimals, Offers, Contact, Customer, \
    MembershipCardOrder, MembershipOrder, Address, Email
from django.contrib.auth import authenticate, login, logout
from home.models import UserCreateFrom

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, User
from .models import Services, OurAnimals, Topslider, Welcometext, Welcomelist, Offers, Contact, Address, Email
from .serializers import (CallSerializer, CategorySerializer, CustomerSerializer, MembershipCardSerializer, MembershipSerializer, OurAnimalsSerializer, ServicesSerializer, SliderSerializer, UserRegistrationSerializer, 
                          WelcomeTextSerializer, WelcomeListSerializer, OffersSerializer, 
                          ContactSerializer, AddressSerializer, EmailSerializer)


# Create your views here.



def home(request):
    slider = Topslider.objects.all()
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




#Get API Views
@api_view(['GET'])
def get_topslider_api(request):
    data = {
        "sliders": Topslider.objects.all(),
       
    }
    return Response({
        "status": "Success",
        "sliders": SliderSerializer(data["sliders"], many=True).data,
    
        
    })


@api_view(['GET'])
def get_welcometext_api(request):
    queryset = Welcometext.objects.all() 
    
    serializer = WelcomeTextSerializer(queryset, many=True)
    
    return Response({
            "status": "Success",
            "welcome_text": serializer.data,
        })

@api_view(['GET'])
def get_welcomelist_api(request):
    data = {
        "welcome_list": Welcomelist.objects.all(),
        
    }
    return Response({
            "status": "Success",

            "welcome_list": WelcomeListSerializer(data["welcome_list"], many=True).data,
            
        })




@api_view(['GET'])
def get_services_api(request):
    data = {

        "services": Services.objects.all(),
    }

    return Response({
        "status": "Success",
        "services": ServicesSerializer(data["services"], many=True).data,
        })

@api_view(['GET'])
def get_call_api(request):
    data = {
        "call": Call.objects.all(),
    }
    return Response({
        "status": "Success",
        "call": CallSerializer(data["call"]).data,
        })

@api_view(['GET'])
def get_category_api(request):
    data = {
        "category": Category.objects.all(),
    }
    return Response({
        "status": "Success",
        "category": CategorySerializer(data["category"], many=True).data,
        })


@api_view(['GET'])
def get_ouranimals_api(request):
    animals_queryset = OurAnimals.objects.all()
    
  
    serializer = OurAnimalsSerializer(animals_queryset, many=True)
    
    return Response({
        "status": "Success",
        "animals": serializer.data,
    })


@api_view(['GET'])
def get_offers_api(request): 
    data = {
        "offers": Offers.objects.all(),
    }
    return Response({
        "status": "Success",
        "offers": OffersSerializer(data["offers"], many=True).data,
        })   


@api_view(['GET'])
def get_membership_api(request):
    data = {
        "membership": MembershipOrder.objects.all(),
    }
    return Response({
        "status": "Success",
        "membership": MembershipSerializer(data["membership"], many=True).data,
        })



@api_view(['GET'])
def get_contact_api(request):
    data = {
         "contact": Contact.objects.all(),
        }
    return Response({
        "status": "Success",
        "contact": ContactSerializer(data["contact"], many=True).data,
        })


@api_view(['GET'])
def get_customer_api(request):
    data = {
         "customer": Customer.objects.all(),
        }
    return Response({
        "status": "Success",
        "customer": CustomerSerializer(data["customer"], many=True).data,
        })


@api_view(['GET'])
def get_UserRegistration_api(request):
    data = {
         "user": User.objects.all(),
        }
    return Response({
        "status": "Success",
        "user": UserRegistrationSerializer(data["user"], many=True).data,
        })


@api_view(['GET'])
def get_membership_card_api(request):
    data = {
         "membership_card": MembershipCardOrder.objects.all(),
        }
    return Response({
        "status": "Success",
        "membership_card": MembershipCardSerializer(data["membership_card"], many=True).data,
        })


@api_view(['GET'])
def get_address_api(request): 
    data = {
         "address": Address.objects.first(),
        }
    return Response({
        "status": "Success",
        "address": AddressSerializer(data["address"]).data,
        })   
         
@api_view(['GET'])
def get_email_api(request):
    data = {
         "email": Email.objects.first(),
        }
    return Response({
        "status": "Success",
        "email": EmailSerializer(data["email"]).data,
        })     
    


#Post API Views
@api_view(['POST'])
def create_topslider_api(request):
    serializer = SliderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Slider created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)
    

@api_view(['POST'])
def create_welcometext_api(request):
    serializer = WelcomeTextSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Welcome text created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)
    

@api_view(['POST'])
def create_welcomelist_api(request):
    serializer = WelcomeListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Welcome list item created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)



@api_view(['POST'])
def create_services_api(request):
    serializer = ServicesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Service created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def create_call_api(request):
    serializer = CallSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Call information created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)



@api_view(['POST'])
def create_category_api(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Category created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)




@api_view(['POST'])
def create_ouranimals_api(request):
    serializer = OurAnimalsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Animal created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def create_offers_api(request):
    serializer = OffersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Offer created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def create_membership_api(request):
    serializer = MembershipSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Membership order created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)




@api_view(['POST'])
def create_contact_api(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Contact information submitted successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)
    

@api_view(['POST'])
def create_customer_api(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Customer created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def create_UserRegistration_api(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "User registered successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def create_membershipCard_api(request):
    serializer = MembershipCardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Membership card order created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def create_address_api(request):
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Address created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)

@api_view(['POST'])
def create_email_api(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Success", "message": "Email created successfully."})
    else:
        return Response({"status": "Error", "message": "Invalid data.", "errors": serializer.errors}, status=400)



#Update API Views...

@api_view(['PATCH'])
def update_topslider_api(request, pk):
    try:
        slider = Topslider.objects.get(pk=pk)
    except Topslider.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = SliderSerializer(slider, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_welcometext_api(request, pk):
    try:
        wtext = Welcometext.objects.get(pk=pk)
    except Welcometext.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = WelcomeTextSerializer(wtext, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_welcomelist_api(request, pk):
    try:
        wlist = Welcomelist.objects.get(pk=pk)
    except Welcomelist.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = WelcomeListSerializer(wlist, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def update_services_api(request, pk):
    try:
        service = Services.objects.get(pk=pk)
    except Services.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = ServicesSerializer(service, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)    


@api_view(['PATCH'])
def update_call_api(request, pk):
    try:
        call = Call.objects.get(pk=pk)
    except Call.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = CallSerializer(call, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)



@api_view(['PATCH'])
def update_category_api(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH']) 
def update_ouranimals_api(request, pk):
    try:
        animal = OurAnimals.objects.get(pk=pk)
    except OurAnimals.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = OurAnimalsSerializer(animal, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def update_offers_api(request, pk):
    try:
        offer = Offers.objects.get(pk=pk)
    except Offers.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = OffersSerializer(offer, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_membership_api(request, pk):
    try:
        membership = MembershipOrder.objects.get(pk=pk)
    except MembershipOrder.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = MembershipSerializer(membership, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)




@api_view(['PATCH'])
def update_contact_api(request, pk): 
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)


    serializer = ContactSerializer(contact, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def update_customer_api(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_UserRegistration_api(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)    


@api_view(['PATCH'])
def update_membership_card_api(request, pk):
    try:
        membership_card = MembershipCardOrder.objects.get(pk=pk)
    except MembershipCardOrder.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = MembershipCardSerializer(membership_card, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_address_api(request, pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = AddressSerializer(address, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_email_api(request, pk):
    try:
        email = Email.objects.get(pk=pk)
    except Email.DoesNotExist:
        return Response({"message": "Not found!"}, status=404)

    serializer = EmailSerializer(email, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Updated", "data": serializer.data})
    return Response(serializer.errors, status=400)




#Delete API Views

@api_view(['DELETE'])
def delete_topslider_api(request, pk):
    try:
        slider = Topslider.objects.get(pk=pk)
        slider.delete()
        return Response({"message": "Slider deleted successfully!"}, status=200)
    except Topslider.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)


@api_view(['DELETE'])
def delete_welcometext_api(request, pk):
    try:
        wtext = Welcometext.objects.get(pk=pk)
        wtext.delete()
        return Response({"message": "Welcome text deleted successfully!"}, status=200)
    except Welcometext.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_welcomelist_api(request, pk):
    try:
        wlist = Welcomelist.objects.get(pk=pk)
        wlist.delete()
        return Response({"message": "Welcome list item deleted successfully!"}, status=200)
    except Welcomelist.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_services_api(request, pk):
    try:
        service = Services.objects.get(pk=pk)
        service.delete()
        return Response({"message": "Service deleted successfully!"}, status=200)
    except Services.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_call_api(request, pk):
    try:
        call = Call.objects.get(pk=pk)
        call.delete()
        return Response({"message": "Call information deleted successfully!"}, status=200)
    except Call.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)        
        
@api_view(['DELETE'])
def delete_category_api(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({"message": "Category deleted successfully!"}, status=200)
    except Category.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_ouranimals_api(request, pk):
    try:
        animal = OurAnimals.objects.get(pk=pk)
        animal.delete()
        return Response({"message": "Animal deleted successfully!"}, status=200)
    except OurAnimals.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_offers_api(request, pk):
    try:
        offer = Offers.objects.get(pk=pk)
        offer.delete()
        return Response({"message": "Offer deleted successfully!"}, status=200)
    except Offers.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_membership_api(request, pk):
    try:
        membership = MembershipOrder.objects.get(pk=pk)
        membership.delete()
        return Response({"message": "Membership order deleted successfully!"}, status=200)
    except MembershipOrder.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)


@api_view(['DELETE'])
def delete_customer_api(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response({"message": "Customer deleted successfully!"}, status=200)
    except Customer.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)



@api_view(['DELETE'])
def delete_contact_api(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        return Response({"message": "Contact deleted successfully!"}, status=200)
    except Contact.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)




@api_view(['DELETE'])
def delete_UserRegistration_api(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully!"}, status=200)
    except User.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)        



@api_view(['DELETE'])
def delete_membership_card_api(request, pk):
    try:
        membership_card = MembershipCardOrder.objects.get(pk=pk)
        membership_card.delete()
        return Response({"message": "Membership card order deleted successfully!"}, status=200)
    except MembershipCardOrder.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)        



@api_view(['DELETE'])
def delete_address_api(request, pk):
    try:
        address = Address.objects.get(pk=pk)
        address.delete()
        return Response({"message": "Address deleted successfully!"}, status=200)
    except Address.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)


@api_view(['DELETE'])
def delete_email_api(request, pk):
    try:
        email = Email.objects.get(pk=pk)
        email.delete()
        return Response({"message": "Email deleted successfully!"}, status=200)
    except Email.DoesNotExist:
        return Response({"message": "It was already not there."}, status=404)










