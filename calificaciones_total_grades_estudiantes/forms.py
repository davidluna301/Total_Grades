from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Calificacion


class CalificacionForm(forms.ModelForm):
	class Meta:
		model = Calificacion
		exclude = ['promedio']
		widgets = {
			'nombre_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
			'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
			'asignatura': forms.TextInput(attrs={'class': 'form-control'}),
			'nota1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00', 'max': '5.00'}),
			'nota2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00', 'max': '5.00'}),
			'nota3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00', 'max': '5.00'}),
		}


class LoginForm(AuthenticationForm):
	username = forms.CharField(
		label='Usuario',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu usuario'}),
	)
	password = forms.CharField(
		label='Contrasena',
		strip=False,
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contrasena'}),
	)
