from django.contrib import admin
from .operaciones import CuentaBancaria, Transaccion

admin.site.register(CuentaBancaria)
admin.site.register(Transaccion)
