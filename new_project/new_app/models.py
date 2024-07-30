from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=11, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return self.email
    

# class Wallet(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     balance = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.user.username} - {self.balance}"

class a_Network(models.Model):
    name = models.CharField(max_length=100)
    variation_code = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.name

class b_DataType(models.Model):
    network = models.ForeignKey(a_Network, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    available = models.BooleanField(default=True, null=True)

    def __str__(self):
        return f'{self.network} - {self.name}'

class c_DataPlan(models.Model):
    network = models.ForeignKey(a_Network, on_delete=models.CASCADE, null=True)
    data_type = models.ForeignKey(b_DataType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    variation_code = models.CharField(max_length=3, null=True)
    validity = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name}'

class DataTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    network = models.ForeignKey(a_Network, on_delete=models.CASCADE)
    data_type = models.ForeignKey(b_DataType, on_delete=models.CASCADE)
    data_plan = models.ForeignKey(c_DataPlan, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=11)
    client_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    webhook_received = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    
    status= models.CharField(max_length=50)
    auto_refund_status = models.CharField(max_length=50)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    reference_no = models.CharField(max_length=50)
    true_response = models.CharField(max_length=50)




