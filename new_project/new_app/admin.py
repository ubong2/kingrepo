from django.contrib import admin
from new_app.models import * 
from import_export.admin import ImportExportModelAdmin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'balance', 'phone_number', 'last_login']
admin.site.register(CustomUser, CustomUserAdmin)


class a_NetworkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name','variation_code']
admin.site.register(a_Network, a_NetworkAdmin)

class b_DataTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['network', 'name', 'available']
admin.site.register(b_DataType, b_DataTypeAdmin)

class c_DataPlanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['network', 'data_type', 'price' , 'variation_code', 'name', 'validity']
admin.site.register(c_DataPlan, c_DataPlanAdmin)

admin.site.register(DataTransaction)