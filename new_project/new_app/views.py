import json
import time
import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from new_app.forms import *
from new_app.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from requests.exceptions import ConnectionError, Timeout, HTTPError
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are already logged in')
        return redirect('index')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Registered Successfully')
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form':form})

def user_login(request):
        if request.user.is_authenticated:
            messages.warning(request, f'{request.user.username}, you are already logged in')
            return redirect('profile')
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                        login(request, user)
                        return redirect("profile")
                else:
                    messages.warning(request, "Invalid login credentials suppiled")
                    return redirect("user_login")
            else:
                messages.warning(request, "Invalid login credentials suppiled")
                return redirect("user_login")
        else:
            form = UserLoginForm()
        return render(request, 'signin.html',{'form':form})


def signout(request):
    logout(request)
    messages.warning(request, 'Logged out')
    return redirect('user_login')

@login_required
def profile(request):
        return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            messages.error(request, "invalid form details")
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'profileEdit.html',{'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,"Your Account Password has been updated successfully")
            return redirect("profile")
        else:
            messages.error(request, "invalid form details")
    else:
        form = CustomPasswordChangeForm(request.POST)
    return render(request,'password_Edit.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'No User found with that email')
            return super().form_invalid(form)

def data_purchase(request):
    if request.method == 'POST':
        form = DataPurchaseForm(request.POST)
        if form.is_valid():
            network = form.cleaned_data['network'].variation_code
            mobile_no = form.cleaned_data['mobile_no']
            data_type = form.cleaned_data['data_type']
            data_plan = form.cleaned_data['data_plan'].variation_code
            client_reference = f"tranx{int(time.time())}"
            amount = form.cleaned_data['data_plan'].price
            
            # Check user wallet balance
            balance_before = request.user.balance
            wallet = CustomUser.objects.get(id=request.user.id)
            if wallet.balance < amount:
                messages.error(request, 'Insufficient Balance')
                return redirect('data_purchase')

            # Deduct from wallet
            wallet.balance -= amount
            wallet.save()
            balance_after = wallet.balance

            try:
                # Make API request
                response = requests.post(
                    'https://easyaccess.com.ng/api/data.php',
                    headers={"AuthorizationToken": "Your_token"},
                    data={
                        'network': network,
                        'mobileno': mobile_no,
                        'dataplan': data_plan,
                        'client_reference': client_reference,
                        'webhook': 'http://127.0.0.1:8000/webhook/'
                    },
                    timeout=60  # Setting a timeout for the request
                )
                
                # Raise an exception for HTTP errors
                response.raise_for_status()
                
                # Parse JSON response
                response_data = response.json()
                auto_refund_status = response_data.get('auto_refund_status', 'Failed')
                
            except ConnectionError:
                messages.error(request, 'Connection error occurred. Please try again later.')
                return handle_refund(wallet, amount, balance_before, balance_after)
                
            except Timeout:
                messages.error(request, 'The request timed out. Please try again later.')
                return handle_refund(wallet, amount, balance_before, balance_after)
                
            except HTTPError as e:
                messages.error(request, f'HTTP error occurred: {e}')
                return handle_refund(wallet, amount, balance_before, balance_after)
                
            except ValueError:
                messages.error(request, 'Invalid response received from the API.')
                return handle_refund(wallet, amount, balance_before, balance_after)
                
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')
                return handle_refund(wallet, amount, balance_before, balance_after)
            
            # Save transaction
            DataTransaction.objects.create(
                user = request.user,
                network=form.cleaned_data['network'],
                data_type = data_type,
                data_plan = form.cleaned_data['data_plan'],
                mobile_no=mobile_no,
                client_reference=client_reference,
                amount=amount,

                status=response_data.get('status', 'Failed'),
                auto_refund_status=response_data.get('auto_refund_status', 'Failed'),
                balance_before = balance_before,
                balance_after = balance_after,
                reference_no = response_data.get('reference_no', 'Failed'),
                true_response = response_data.get('true_response', 'Failed'),
            )
            if auto_refund_status.lower() == 'failed':
                messages.error(request, 'Purchase failed!')
                return handle_refund(wallet, amount, balance_before, balance_after)

            messages.success(request, 'Data purchase successful!')
            return redirect('data_purchase')
    else:
        form = DataPurchaseForm() 
    return render(request, 'buyData.html', {'form': form})

def handle_refund(wallet, amount, balance_before, balance_after):
    # Refund user's wallet
    balance_before = balance_after
    wallet.balance += amount
    wallet.save()
    # Adjust balance_after in the transaction
    balance_after = wallet.balance
    return redirect('data_purchase')


def ajax_load_data_types(request):
    network_id = request.GET.get('network')
    data_types = b_DataType.objects.filter(network_id=network_id, available=True)#.order_by('name')
    return render(request, 'data_type.html', {'data_types': data_types})

def ajax_load_data_plans(request):
    data_type_id = request.GET.get('data_type')
    data_plans = c_DataPlan.objects.filter(data_type_id=data_type_id).order_by('id')
    return render(request, 'data_plan.html', {'data_plans': data_plans})

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_reference = data.get('client_reference')
        
        try:
            transaction = DataTransaction.objects.get(client_reference=client_reference)
        except DataTransaction.DoesNotExist:
            transaction = None
            return HttpResponse({"status": "received"})
        
        if transaction:
            transaction.status = data.get('status')
            transaction.webhook_received = True
            transaction.save()
        
        # return JsonResponse({"status": "received"})
        return HttpResponse({"status": "received"})
    
def switch_pdt(request):
    types = b_DataType.objects.all()
    return render(request, 'switch.html', {'types': types})

def data_on(request, id):
    types = b_DataType.objects.get(id=id)
    types.available=True
    types.save()
    messages.success(request, 'Product Switched On')
    return redirect('switch_pdt')

def data_of(request, id):
    types = b_DataType.objects.get(id=id)
    types.available=False
    types.save()
    messages.warning(request, 'Product Switched Off')
    return redirect('switch_pdt')

def transaction_history(request):
    transactions = DataTransaction.objects.filter(user=request.user).order_by('-transaction_date')
    return render(request, 'transaction_history.html', {'transactions': transactions})