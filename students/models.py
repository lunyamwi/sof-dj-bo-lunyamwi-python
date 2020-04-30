from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from datetime import datetime
from django.utils.timezone import datetime, timedelta
import django.utils.timezone
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

import stripe
stripe.api_key=settings.STRIPE_SECRET_KEY

# Create your models here.
MEMBERSHIP_CHOICES=(
    ('Enterprise','ent'),
    ('Professional','pro'),
    ('Free','free')
)

class Membership(models.Model):
    slug=models.SlugField()
    membership_type=models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30
    )
    price=models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)


    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_customer_id=models.CharField(max_length=40)
    membership = models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.user.username

def post_save_usermembership_create(sender,instance,created,*args,**kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)

    user_membership, created = UserMembership.objects.get_or_create(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        new_customer_id=stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.save()

post_save.connect(post_save_usermembership_create,sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_membership=models.ForeignKey(UserMembership,on_delete=models.CASCADE)
    stripe_subscription_id=models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)



# Create your models here.
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, *args, **kwargs):
        """Create and return a `User` with an email, username and password."""
        password = kwargs.get('password', '')
        email = kwargs.get('email', '')
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    first_name = models.CharField(db_index=True, max_length=255, unique=False)

    last_name = models.CharField(db_index=True, max_length=255, unique=False)

    username = models.CharField(default=first_name,max_length=255)
    
    email = models.EmailField(db_index=True, unique=True)

    is_superuser = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    date_of_birth = models.DateTimeField(null=True,blank=True,default=django.utils.timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.first_name