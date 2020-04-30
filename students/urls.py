from django.urls import path
from .views import (
    MembershipCreateView,
    MembershipSelectView,
    PaymentView,
    updateTransactions,
    profile_view,
    cancel_subscription,
    UserCreateView,
    UserLoginCreateView, 
    UserRegistrationCreateView,
    logout_view
)

app_name='members'

urlpatterns=[   
    path('',MembershipSelectView.as_view(),name='select'),
    path('user/membership/create/',UserCreateView.as_view(),name='create-user'),
    path('members/create/',MembershipCreateView.as_view(),name='create'),
    path('members/login/', UserLoginCreateView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', UserRegistrationCreateView.as_view(), name='sign_up'),
    path('payment/',PaymentView,name='payment'),
    path('update-transactions/<subscription_id>/',updateTransactions,name='update-transactions'),
    path('profile/',profile_view,name='profile'),
    path('cancel/',cancel_subscription,name='cancel'),
]