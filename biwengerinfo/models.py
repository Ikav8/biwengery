from django.db import models

# Create your models here.

class Jugador(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    equipo = models.CharField(max_length=50, null=False, blank=False)
    dinero_inicial = models.IntegerField(default=0)
    dinero = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre + " (" + self.equipo + ") -> " + str(self.dinero)

class Movimiento(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    balance = models.IntegerField(null=False, blank=False)
    detalles = models.CharField(max_length=200, null=False, blank=True)

    def __str__(self):
        signo = '+' if self.balance > 0 else '-'
        return("[" + signo + "] " + self.jugador + " [ " + str(self.balance) + " ] (" + self.detalles + ").")