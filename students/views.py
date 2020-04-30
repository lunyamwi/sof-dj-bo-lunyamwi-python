from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.views.generic import ListView,CreateView,FormView
from .models import Membership,UserMembership,Subscription,User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.mail import send_mail
from .forms import UserSignupForm, UserLoginForm


# Create your views here.
import stripe

def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context={
        'user_membership':user_membership,
        'user_subscription':user_subscription
    }
    return render(request,'students/profile.html',context)

def get_user_membership(request):
    user_membership_qs=UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None 

def get_user_subscription(request):
    user_subscription_qs=Subscription.objects.filter(
        user_membership=get_user_membership(request)
    )
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs=Membership.objects.filter(
            membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


def logout_view(request):
    logout(request)
    return redirect('members:login')

class MembershipCreateView(CreateView):
    model = Membership
    fields = ['slug','membership_type','price','stripe_plan_id',]
    success_url = reverse_lazy('courses:list')

class UserCreateView(CreateView):
    model = UserMembership
    fields = ['user','stripe_customer_id','membership',]
    success_url = reverse_lazy('courses:list')


class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self,request,**kwargs):
        selected_membership_type=request.POST.get('membership_type')
        
        user_membership =get_user_membership(request)
        user_subscription=get_user_subscription(request)
        
        selected_membership_qs=Membership.objects.filter(
            membership_type=selected_membership_type
        )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()

        '''
        ==========
        Validation
        ==========
        '''

        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request,"You already have this membership. Your \
                next payment is due {}".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('members:payment'))


def PaymentView(request):
    user_membership=get_user_membership(request)
    selected_membership=get_selected_membership(request)
    publishKey= settings.STRIPE_PUBLISHABLE_KEY

    if request.method == "POST":
        try:
            token = request.POST['stripeToken']
            cus = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            cus.source = token
            cus.save()
            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[{"plan": selected_membership.stripe_plan_id}],
            )
        except stripe.error.CardError as e:
            messages.info(request,"Your card has been declined")
        return redirect(reverse('members:update-transactions',
                kwargs={
                    'subscription_id':subscription.id
                }))

    context = {
        'publishKey':publishKey,
        'selected_membership':selected_membership
    }

    return render(request,"students/membership_payments.html",context)



def updateTransactions(request,subscription_id):
    
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    user_membership.membership = selected_membership
    user_membership.save()

    sub,created = Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active=True
    sub.save()

    try:
        del request.session['selected_mebership_type']
    except:
        pass


    messages.info(request,"successfully created {} membership".format(selected_membership))
    return redirect('/')

def cancel_subscription(request):
    user_subscription = get_user_subscription(request)

    if user_subscription.active == False:
        messages.info(request,"You don't have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
 
    sub = stripe.Subscription.retrieve(user_subscription.stripe_subscription_id)
    sub.delete()

    user_subscription.active = False
    user_subscription.save()

    free_membership = Membership.objects.filter(membership_type='Free').first()
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    messages.info(request,"Successfully cancelled membership. We have sent an email")

    # sending an email here

    return redirect('members:select')

class UserRegistrationCreateView(FormView):
    """
    Create user api view
    """
    model = User
    form_class = UserSignupForm
    template_name = 'students/register.html'

    def post(self, request):
        """
        Overide the default post()
        """
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        data = {
            "first_name": form.cleaned_data['first_name'],
            "last_name": form.cleaned_data['last_name'],
            "password": form.cleaned_data['password'],
            "email": form.cleaned_data['email'],
            "date_of_birth": form.cleaned_data['date_of_birth'],
        }
        User.objects.create_user(**data)
        return redirect(reverse('members:login'))


class UserLoginCreateView(FormView):
    """
    Create user api view
    """
    model = User
    form_class = UserLoginForm
    template_name = 'students/login.html'
    success_url = reverse_lazy("courses:list")

    def post(self, request):
        """
        Overide the default post()
        # """
        form = self.form_class(request.POST)
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user and user.is_active:
            login(request, user)
            return super(UserLoginCreateView, self).form_valid(form)
        messages.success(request, 'This email and password combination is invalid', extra_tags='red')
        return render(request, self.template_name, {"form": form})

