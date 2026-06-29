from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Address

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'address_list.html', {'addresses': addresses, 'active_nav': 'address'})

@login_required
def address_add(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            label=request.POST.get('label', 'other'),
            name=request.POST['name'],
            phone=request.POST['phone'],
            province=request.POST['province'],
            city=request.POST['city'],
            district=request.POST['district'],
            detail=request.POST['detail'],
        )
        messages.success(request, '地址添加成功')
        return redirect('address_list')
    return render(request, 'address_form.html', {'title': '新增地址', 'active_nav': 'address'})

@login_required
def address_edit(request, addr_id):
    addr = get_object_or_404(Address, id=addr_id, user=request.user)
    if request.method == 'POST':
        addr.label = request.POST.get('label', 'other')
        addr.name = request.POST['name']
        addr.phone = request.POST['phone']
        addr.province = request.POST['province']
        addr.city = request.POST['city']
        addr.district = request.POST['district']
        addr.detail = request.POST['detail']
        addr.save()
        messages.success(request, '地址已更新')
        return redirect('address_list')
    return render(request, 'address_form.html', {'addr': addr, 'title': '编辑地址', 'active_nav': 'address'})

@login_required
def address_delete(request, addr_id):
    addr = get_object_or_404(Address, id=addr_id, user=request.user)
    addr.delete()
    messages.success(request, '地址已删除')
    return redirect('address_list')
