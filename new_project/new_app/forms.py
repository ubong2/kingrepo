from django import forms  
from new_app.models import * 
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

  
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control mt-2',}),
        label='Email',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mt-2',}),
        label='Password',
    )


class CustomUserCreationForm(UserCreationForm):
    # first_name =forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your First name", "class": "form-control border-2"}))
    # last_name =forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your Last name", "class": "form-control border-2"}))
    # phone_number =forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your Phone umber", "class": "form-control border-2"}))
    email =forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter your Email", "class": "form-control border-2"}))
    password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control border-2"}))
    password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control border-2"}))
 
    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

class UpdateProfileForm(forms.ModelForm):
    first_name =forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your First name", "class": "form-control border-2"}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your Last name", "class": "form-control border-2"}))
    phone_number =forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your Phone umber", "class": "form-control border-2"}))
    # email =forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter your Email", "class": "form-control border-2", "required": "required",
    #             "autofocus": "autofocus, "readonly": "readonly","}))
 
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", 'phone_number']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control border-2'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control border-2'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control border-2'}), label="Confirm New Password")
    class Meta:
        model = CustomUser
        fields = ('old_password','new_password1', 'new_password2')

class DataPurchaseForm(forms.ModelForm):
    network = forms.ModelChoiceField(
        queryset = a_Network.objects.all(),
        # empty_label = "",
        widget = forms.Select(attrs={'class': 'form-select border-2 bg-body-tertiary'}),
        required = True,
    )
    data_type = forms.ModelChoiceField(
        queryset = b_DataType.objects.none(),
        # empty_label="",
        widget = forms.Select(attrs={'class': 'form-select border-2 bg-body-tertiary'}),
        required = True,
    )
    data_plan = forms.ModelChoiceField(
        queryset = c_DataPlan.objects.none(),
        # empty_label="",
        widget = forms.Select(attrs={'class': 'form-select border-2 bg-body-tertiary'}),
        required = True,
        )
    mobile_no =forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control border-2 bg-body-tertiary"}),
        )
    class Meta:
        model = DataTransaction
        fields = ['network', 'data_type', 'data_plan', 'mobile_no']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_type'].queryset = b_DataType.objects.none()
        self.fields['data_plan'].queryset = c_DataPlan.objects.none()

        if 'network' in self.data:
            try:
                network_id = int(self.data.get('network'))
                self.fields['data_type'].queryset = b_DataType.objects.filter(network_id=network_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'data_type' in self.data:
            try:
                data_type_id = int(self.data.get('data_type'))
                self.fields['data_plan'].queryset = c_DataPlan.objects.filter(data_type_id=data_type_id).order_by('name')
            except (ValueError, TypeError):
                pass
