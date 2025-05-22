from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistroForm
from .operaciones import CuentaBancaria, Transaccion
from django.contrib.auth.models import User


def crear_cuenta(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "¡Usuario creado exitosamente!")
            return redirect('iniciar_sesion')
        else:
            messages.error(request, "Hubo un error en el formulario.")
    else:
        form = RegistroForm()
    
    return render(request, 'gestor/signin.html', {'form': form})


def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pagina_principal')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'gestor/login.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')


@login_required(login_url='iniciar_sesion')
def pagina_principal(request):
    cuentas = CuentaBancaria.objects.filter(usuario=request.user)
    return render(request, 'gestor/home.html', {'cuentas': cuentas})


@login_required(login_url='iniciar_sesion')
def crear_cuenta_bancaria(request):
    if CuentaBancaria.objects.filter(usuario=request.user).count() < 2:
        nueva_cuenta = CuentaBancaria(usuario=request.user)
        nueva_cuenta.save()
        messages.success(request, "¡Cuenta creada exitosamente!")
    else:
        messages.error(request, "Solo puedes tener un máximo de 2 cuentas bancarias.")
    return redirect('pagina_principal')


@login_required(login_url='iniciar_sesion')
def detalle_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    transacciones = cuenta.transacciones.all()
    return render(request, 'gestor/account_detail.html', {
        'cuenta': cuenta,
        'transacciones': transacciones
    })


@login_required(login_url='iniciar_sesion')
def depositar_dinero(request, cuenta_id):
    if request.method == "POST":
        cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
        monto = Decimal(request.POST['monto'])
        if monto > 0:
            cuenta.balance += monto
            cuenta.save()
            Transaccion.objects.create(cuenta=cuenta, tipo='Depósito', monto=monto)
            messages.success(request, f"Se han depositado ${monto} a tu cuenta.")
        else:
            messages.error(request, "El monto debe ser mayor a cero.")
        return redirect('detalle_cuenta', cuenta_id=cuenta.id)


@login_required(login_url='iniciar_sesion')
def transferir_dinero(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    
    if request.method == "POST":
        numero_cuenta_destino = request.POST['numero_cuenta']
        monto = Decimal(request.POST['monto'])
        concepto = request.POST['concepto']

        if monto <= 0:
            messages.error(request, "El monto debe ser mayor a cero.")
            return redirect('transferir_dinero', cuenta_id=cuenta.id)

        if monto <= cuenta.balance:
            cuenta.balance -= monto
            cuenta.save()
            Transaccion.objects.create(
                cuenta=cuenta,
                tipo='Transferencia',
                monto=monto,
                referencia=f"{numero_cuenta_destino} - {concepto}"
            )
            messages.success(request, f"Transferencia exitosa de ${monto} a {numero_cuenta_destino}.")
            return redirect('detalle_cuenta', cuenta_id=cuenta.id)
        else:
            messages.error(request, "Saldo insuficiente para realizar la transferencia.")
            return redirect('transferir_dinero', cuenta_id=cuenta.id)
    
    return render(request, 'gestor/transfer.html', {'cuenta': cuenta})


@login_required(login_url='iniciar_sesion')
def detalles_usuario(request):
    if request.method == 'POST':
        if 'update' in request.POST:
            request.user.username = request.POST.get('username')
            request.user.email = request.POST.get('email')
            password = request.POST.get('password')
            if password:
                request.user.set_password(password)
            request.user.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('detalles_usuario')
        
        if 'delete' in request.POST and request.POST.get('confirm') == "YES":
            Transaccion.objects.filter(cuenta__usuario=request.user).delete()
            CuentaBancaria.objects.filter(usuario=request.user).delete()
            request.user.delete()
            messages.success(request, 'Usuario y todas sus cuentas fueron eliminados.')
            return redirect('iniciar_sesion')
    
    return render(request, 'gestor/user_detail.html')
