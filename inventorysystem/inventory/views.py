from django.shortcuts import render, get_object_or_404,redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm,UpdateInventoryForm
from django.contrib import messages
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json

@login_required
def Inventory_list(request):
    inventories=Inventory.objects.all()
    context={
       "title": "Inventory List",
       "inventories":inventories
    }
    return render(request,'inventory_list.html',context=context)

@login_required
def per_product_view(request,id):
    inventory=get_object_or_404(Inventory,id=id)
    context={
       'inventory': inventory
      }
    return render(request,'per_product.html',context=context)

@login_required
def add_product(request):
    if request.method =="POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory=add_form.save(commit=False)
            cost_per_item = float(add_form.cleaned_data['cost_per_item'])
            quantity_in_sold = float(add_form.cleaned_data['quantity_in_sold'])
            new_inventory.sales = cost_per_item * quantity_in_sold
            new_inventory.save()
            messages.success(request,'successfully added product')
            return redirect('/inventory/')
        
    else:
        add_form=AddInventoryForm()
    return render(request,'inventory_add.html',{'form': add_form})

@login_required
def delete_inventory(request,id):
    inventory=get_object_or_404(Inventory,id=id)
    inventory.delete()
    messages.success(request,'Delete Inventory Succesfully')
    return redirect('/inventory/')

@login_required
def update_inventory(request,id):
    inventory=get_object_or_404(Inventory,id=id)
    if request.method=='POST':
        updateform=UpdateInventoryForm(data=request.POST)
        if updateform.is_valid():
            inventory.name=updateform.data['name']
            inventory.quantity_in_stock=updateform.data['quantity_in_stock']
            inventory.quantity_in_sold=updateform.data['quantity_in_sold']
            inventory.cost_per_item = float(updateform.data['cost_per_item'])
            inventory.sales=float(inventory.cost_per_item)* float(inventory.quantity_in_sold)
            inventory.save()
            messages.success(request,'Update Inventory Succesfully')
            return redirect(f'/inventory/per_product/{id}')
    else:
        updateform=UpdateInventoryForm(instance=inventory)
        context={'form':updateform}
        return render(request,'inventory_update.html',context=context)
    
def dashboard(request):
    inventories=Inventory.objects.all()
    df= read_frame(inventories)
    # print(df)
    sales_graph=df.groupby(by='last_sales_date',as_index=False,sort=False)['sales'].sum()
    sales_graph=px.line(sales_graph,x=sales_graph.last_sales_date,y=sales_graph.sales,title='Sales Trend')
    sales_graph=json.dumps(sales_graph,cls=plotly.utils.PlotlyJSONEncoder)
    # print(sales_graph)

    context={
        "sales_graph":sales_graph
    }
    return render(request,'dashboard.html',context=context)


