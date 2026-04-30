from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, RedirectView, TemplateView, UpdateView

from .forms import CalificacionForm, LoginForm
from .models import Calificacion


def get_user_role(user):
	if not user.is_authenticated:
		return None
	if user.is_superuser:
		return 'superadmin'
	if user.groups.filter(name='profesor').exists():
		return 'profesor'
	if user.groups.filter(name='estudiante').exists():
		return 'estudiante'
	return None


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
	allowed_roles = []

	def test_func(self):
		return get_user_role(self.request.user) in self.allowed_roles

	def handle_no_permission(self):
		if not self.request.user.is_authenticated:
			return super().handle_no_permission()
		return redirect('dashboard')


class HomeView(TemplateView):
	template_name = 'calificaciones/home.html'


class RoleLoginView(FormView):
	template_name = 'calificaciones/login.html'
	form_class = LoginForm

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('dashboard')
		return super().dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

	def form_valid(self, form):
		login(self.request, form.get_user())
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('dashboard')


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
	permanent = False

	def get_redirect_url(self, *args, **kwargs):
		role = get_user_role(self.request.user)
		if role == 'superadmin':
			return reverse('superadmin_dashboard')
		if role == 'profesor':
			return reverse('profesor_dashboard')
		return reverse('estudiante_dashboard')


class SuperadminDashboardView(RoleRequiredMixin, TemplateView):
	template_name = 'calificaciones/dashboard_superadmin.html'
	allowed_roles = ['superadmin']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['total_calificaciones'] = Calificacion.objects.count()
		context['promedio_general'] = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg']
		context['total_estudiantes'] = Calificacion.objects.values('identificacion').distinct().count()
		context['total_profesores'] = self.request.user.__class__.objects.filter(groups__name='profesor').distinct().count()
		context['calificaciones_recientes'] = Calificacion.objects.order_by('-id')[:5]
		return context


class ProfesorDashboardView(RoleRequiredMixin, TemplateView):
	template_name = 'calificaciones/dashboard_profesor.html'
	allowed_roles = ['profesor']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['total_calificaciones'] = Calificacion.objects.count()
		context['promedio_general'] = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg']
		context['asignaturas_activas'] = Calificacion.objects.values('asignatura').distinct().count()
		context['calificaciones_recientes'] = Calificacion.objects.order_by('-id')[:8]
		return context


class EstudianteDashboardView(RoleRequiredMixin, TemplateView):
	template_name = 'calificaciones/dashboard_estudiante.html'
	allowed_roles = ['estudiante']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		calificaciones = Calificacion.objects.filter(identificacion=self.request.user.username).order_by('asignatura')
		context['calificaciones'] = calificaciones
		context['promedio_personal'] = calificaciones.aggregate(Avg('promedio'))['promedio__avg']
		context['total_materias'] = calificaciones.count()
		return context


class CalificacionListView(LoginRequiredMixin, ListView):
	model = Calificacion
	template_name = 'calificaciones/listar.html'
	context_object_name = 'calificaciones'

	def get_queryset(self):
		role = get_user_role(self.request.user)
		queryset = Calificacion.objects.order_by('nombre_estudiante', 'asignatura')
		if role == 'estudiante':
			return queryset.filter(identificacion=self.request.user.username)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		calificaciones = context['calificaciones']
		role = get_user_role(self.request.user)
		context['role_name'] = role
		context['promedio_general'] = calificaciones.aggregate(Avg('promedio'))['promedio__avg']
		context['can_create'] = role in ['superadmin', 'profesor']
		context['can_edit'] = role in ['superadmin', 'profesor']
		context['can_delete'] = role == 'superadmin'
		return context


class CalificacionCreateView(RoleRequiredMixin, CreateView):
	model = Calificacion
	form_class = CalificacionForm
	template_name = 'calificaciones/crear.html'
	success_url = reverse_lazy('listar')
	allowed_roles = ['superadmin', 'profesor']


class CalificacionUpdateView(RoleRequiredMixin, UpdateView):
	model = Calificacion
	form_class = CalificacionForm
	template_name = 'calificaciones/editar.html'
	success_url = reverse_lazy('listar')
	allowed_roles = ['superadmin', 'profesor']


class CalificacionDeleteView(RoleRequiredMixin, DeleteView):
	model = Calificacion
	template_name = 'calificaciones/eliminar.html'
	success_url = reverse_lazy('listar')
	allowed_roles = ['superadmin']


class PromedioGeneralView(RoleRequiredMixin, TemplateView):
	template_name = 'calificaciones/promedio_general.html'
	allowed_roles = ['superadmin', 'profesor']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['promedio_general'] = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg']
		return context
