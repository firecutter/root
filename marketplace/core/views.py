from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ProductForm

@login_required
def create_product(request):
    if request.user.user_type != "Vendedor":
        return HttpResponseForbidden("Apenas vendedores podem cadastrar produtos.")
    
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')  # Substitua 'product_list' pela URL da lista de produtos
    else:
        form = ProductForm()
    
    return render(request, 'create_product.html', {'form': form})