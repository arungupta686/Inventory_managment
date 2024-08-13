from django.urls import path
from .views import Inventory_list,per_product_view,add_product,delete_inventory,update_inventory,dashboard
urlpatterns=[
  path('', Inventory_list,name='inventory_list.html'),
  path('per_product/<int:id>/', per_product_view,name='per_product.html'),
  path('add_product/',add_product,name='inventory_add.html'),
  path('delete/<int:id>',delete_inventory,name="delete_inventory"),
  path('update/<int:id>',update_inventory,name="update_inventory"),
  path('dashboard/',dashboard,name='dashboard')



 ]