from django.shortcuts import render, redirect
from .models import Customuser
from django import forms
from .forms import UserRegisterForm, Overall_Form, LoginForm, Disabled_Form
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bio
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, View
from django.http import HttpResponse
from .utils import render_to_pdf
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

"""def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        custom_user = Customuser.objects.filter(email=username)
        custom_user = authenticate(request, username=username, password=password)
        if custom_user is not None:
            login(request, custom_user)
            print('user has been logged in')
            return redirect('choice')
        else:
            print('else portion')

    return render(request, 'registerapp/login2.html')


"""
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)


            #custom_user = Customuser.objects.filter(email=username)
            custom_user = authenticate(request, username=username, password=password)
            if custom_user is not None:
                login(request, custom_user)
                print('user has been logged in')
                return redirect('choice')
            elif custom_user is None:
                print('message section')
                messages.warning(request, 'Password or email address is incorrect')
            print(custom_user)
        else:
            print('else portion')
        #print(username)
        #print(password)
    else:
        form = LoginForm()
        print('this is a get request')
    return render(request, 'registerapp/login2.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = Customuser.objects.create_user(email, email, password)
            user.is_active = False
            user.save()
            messages.success(request,
                             f'Account created for Applicant with the email address: {email}! ')
            current_site = get_current_site(request)
            subject = 'Activate Your Registration Account'
            message = render_to_string('registerapp/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            mail = EmailMessage(subject, message, to=[email])
            mail.send()
            return redirect('account_activation_sent')

    else:
        form = UserRegisterForm()
        print('a get request')
    return render(request, 'registerapp/register.html', {'form':form} )

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customuser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customuser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('choice')
    else:
        return render(request, 'registerapp/invalid_activation.html')


def account_activation_sent(request):
    return render(request, 'registerapp/confirmation_sent.html')

class GeneratePdf(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        bio_pk = self.request.user.bio.pk
        print(bio_pk)
        my_bio = Bio.objects.filter(pk = bio_pk).first()
        print(my_bio)
        template = get_template('registerapp/printout.html')
        context = {
            "my_bio": my_bio}
        html = template.render(context)
        pdf = render_to_pdf('registerapp/printout.html', context)
        return HttpResponse(pdf, content_type='application/pdf')






def homepage(request):
    return render(request, 'registerapp/homepage.html')

@login_required()
def success(request):
    return render(request, 'registerapp/success.html')



class BioCreateView(LoginRequiredMixin, CreateView):
    model = Bio
    form_class = Overall_Form
    mod = get_user_model()
    print(mod)
    """def check_first(self):
        if self.request.user.bio.submitted == True:
            messages.success(request, f'An Application has been submitted already for this user, {self.request.user} '

            return redirect('choice') """


    def form_valid(self, form):
        #overwriting the form_valid method to make the author of the post to be the user that sends the post request on the form
        all_reg = Bio.objects.all().filter(submitted=True)
        all_email = []
        for i in all_reg:
            my_email = i.user.username
            all_email.append(my_email)
        user_email = self.request.user
        print('user\'s email : {}'.format(user_email))
        print('all email : {}'.format(all_email))
        if user_email not in all_email:
            the_user = self.request.user
            form.instance.user = self.request.user
            form.instance.user.submitted = True
            form.instance.submitted = True
            self.request.user.submitted = True
            the_user.submitted = True
            the_user.save()
            print('self.request.user : {}'.format(self.request.user))
            print('self.request.user.submitted : {}'.format(self.request.user.submitted))
            print('first condition satisfied')
            return super().form_valid(form)
        else:
            print('second condition satisfied')
            messages.warning(request, 'Application has already been submitted before')
            return redirect('/')

class BioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bio
    form_class = Disabled_Form

    def form_valid(self, form):
        #overwriting the form_valid method to make the author of the post to be the user that sends the post request on the form
        form.instance.user = self.request.user
        self.request.user.submitted = True
        #after obtaining tha author of the post...run the form_valid method on the parent class
        return super().form_valid(form)

    def test_func(self):
        bio = self.get_object()
        if self.request.user.username == bio.user.username:
            return True
        else:
            return False

@login_required
def choice(request):

    if request.user.submitted == True:
        pk = request.user.bio.pk
        print(pk)
        #obj = get_object_or_404(Bio, pk=pk)
        context={'pk' : pk}
        return render(request, 'registerapp/choice.html', context)
    else:
        return render(request, 'registerapp/choice.html')

    return render(request, 'registerapp/choice.html')


