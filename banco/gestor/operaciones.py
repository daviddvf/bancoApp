from django.db import models
from django.contrib.auth.models import User
import uuid

class CuentaBancaria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuentas')
    numero_cuenta = models.CharField(max_length=20, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.numero_cuenta:
            self.numero_cuenta = self.generar_numero_cuenta()
        super(CuentaBancaria, self).save(*args, **kwargs)

    def generar_numero_cuenta(self):
        while True:
            nuevo_numero = uuid.uuid4().hex[:10]
            if not CuentaBancaria.objects.filter(numero_cuenta=nuevo_numero).exists():
                return nuevo_numero

    def __str__(self):
        return f"{self.numero_cuenta} - {self.usuario.username}"


class Transaccion(models.Model):
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='transacciones')
    tipo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto} - {self.cuenta.numero_cuenta}"
