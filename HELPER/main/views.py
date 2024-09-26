from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from .SupportPrograms.crypto_parser import cryptocurrency_rate_parser
from .SupportPrograms.share_parser import share_rate_parser

class HomePageView(View):

    def get(self, request):

        if request.user.is_authenticated:

            sum = 0
            share_list = models.Share.objects.filter(owner=request.user)
            crypto_list = models.Crypto.objects.filter(owner=request.user)

            for crypto in crypto_list:
                if (result := cryptocurrency_rate_parser(crypto.name)):
                    sum += result * crypto.amount

            for share in share_list:
                if (result := share_rate_parser(share.ticker)):
                    sum += result * share.amount

            data = {
                'username': request.user.username,
                'sum': round(sum, 2)
                }

            return render(request, 'main/home_page_user.html', data)
        else:
            return render(request, 'main/home_page.html')
    



class BaseAssetPageView(View):
    model = None  
    form_class = None  
    parser_function = None  
    template_name = ''  

    def calculate_total(self, owner):
        total_sum = 0
        assets = self.model.objects.filter(owner=owner)

        for asset in assets:

            is_exists = False
            result = None

            if self.model == models.Crypto:
                if (result := cryptocurrency_rate_parser(asset.name)):
                    is_exists = True
                    result = result

            elif self.model == models.Share:
                if (result := share_rate_parser(asset.ticker)):
                    is_exists = True
                    result = result

            if is_exists:
                total_sum += result * asset.amount
                asset.price = round(result, 2)
                asset.total_value = round(result * asset.amount, 2)

        return assets, total_sum

    def get(self, request):
        if request.user.is_authenticated:
            assets, total_sum = self.calculate_total(request.user)

            data = {
                'assets': assets,
                'form': self.form_class,
                'sum': round(total_sum, 2)
            }
            return render(request, self.template_name, data)
        else:
            return redirect('home_page')

    def post(self, request):
        if request.POST.get('delete_name'):
            asset = self.model.objects.filter(owner=request.user, name=request.POST.get('delete_name')).first()
            if asset:
                asset.delete()
            return redirect(f'/{self.model.__name__.lower()}_manage/')
        
        form = self.form_class(data=request.POST)

        if form.is_valid():

            asset_name = None

            if self.model == models.Crypto:
                asset_name = form.cleaned_data['name']

            elif self.model == models.Share:
                asset_name = form.cleaned_data['ticker']

            # if not self.parser_function(str(asset_name)):
            #     return redirect(f'{self.model.__name__.lower()}_page')

            asset, created = self.model.objects.get_or_create(
                owner=request.user,
                name=asset_name,
                defaults={
                    'ticker': str(form.cleaned_data['ticker']).upper(),
                    'amount': form.cleaned_data['amount']
                }
            )
            if not created:
                asset.amount += form.cleaned_data['amount']
                asset.save()
            return redirect(f'{self.model.__name__.lower()}_page')

        return redirect(f'{self.model.__name__.lower()}_page')



class CryptoPageView(BaseAssetPageView):
    model = models.Crypto
    form_class = forms.CryptoForm
    parser_function = cryptocurrency_rate_parser
    template_name = 'main/crypto_page.html'



class SharePageView(BaseAssetPageView):
    model = models.Share
    form_class = forms.ShareForm
    parser_function = share_rate_parser
    template_name = 'main/share_page.html'



class RegisterPageView(CreateView):
    template_name = 'main/register_page.html'
    model = User
    form_class = forms.CustomUserCreationForm
    success_url = '/login/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    


class LoginPageView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return render(request, 'main/login_page.html', {'form': AuthenticationForm()})
        else:
            return redirect('home_page')
    
    def post(self, request):
        if not request.user.is_authenticated:

            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)  
                    return redirect('home_page')  
            return render(request, 'main/login_page.html', {'form': form})
        
        else:
            return redirect('home_page')
    

class LogoutView(View):
    def get(self, request):

        if request.user.is_authenticated:
            logout(request)
            return redirect('home_page')
        else:
            return redirect('home_page')