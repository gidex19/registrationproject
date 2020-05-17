from django.urls import path
from . import views as reg_views

urlpatterns = [
    path('', reg_views.homepage, name = 'homepage'),
    path('register/', reg_views.register, name='register'),
    path('login/', reg_views.login_page, name='login'),
    path('bio/new/', reg_views.BioCreateView.as_view(), name = 'bio-create'),
    path('bio/<int:pk>/update', reg_views.BioUpdateView.as_view(), name = 'bio-update'),
    path('choice/', reg_views.choice, name = 'choice'),
    path('success/', reg_views.success, name = 'success'),
    path('success/pdf/', reg_views.GeneratePdf.as_view(), name = 'pdf'),
    path('account_activation_sent/', reg_views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/',reg_views.activate, name='activate'),
    path('invalid_activation/', reg_views.activate, name='invalid_activation'),
]

