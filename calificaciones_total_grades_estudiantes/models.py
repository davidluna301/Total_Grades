from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Calificacion(models.Model):
	nota_validators = [
		MinValueValidator(Decimal('0.00')),
		MaxValueValidator(Decimal('5.00')),
	]

	nombre_estudiante = models.CharField(max_length=150)
	identificacion = models.CharField(max_length=15)
	asignatura = models.CharField(max_length=100)
	nota1 = models.DecimalField(max_digits=5, decimal_places=2, validators=nota_validators)
	nota2 = models.DecimalField(max_digits=5, decimal_places=2, validators=nota_validators)
	nota3 = models.DecimalField(max_digits=5, decimal_places=2, validators=nota_validators)
	promedio = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

	def calcular_promedio(self):
		return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)

	def save(self, *args, **kwargs):
		self.promedio = self.calcular_promedio()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.nombre_estudiante} - {self.asignatura}"
