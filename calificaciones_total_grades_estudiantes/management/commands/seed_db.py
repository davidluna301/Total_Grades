from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from calificaciones_total_grades_estudiantes.models import Calificacion


class Command(BaseCommand):
    help = 'Seed the database with demo users and sample grades'

    def add_arguments(self, parser):
        parser.add_argument(
            '--grades',
            action='store_true',
            help='Also seed sample Calificacion records',
        )

    def handle(self, *args, **options):
        # --- Groups ---
        Group.objects.get_or_create(name='profesor')
        Group.objects.get_or_create(name='estudiante')

        users_data = [
            {
                'username': 'superadmin',
                'password': 'SuperAdmin2026!',
                'is_superuser': True,
                'is_staff': True,
                'group': None,
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': 'superadmin',
            },
            {
                'username': 'profesor1',
                'password': 'Profesor2026!',
                'is_superuser': False,
                'is_staff': True,
                'group': 'profesor',
                'first_name': 'Laura',
                'last_name': 'Docente',
                'role': 'profesor',
            },
            {
                'username': 'profesor2',
                'password': 'Profesor2026!',
                'is_superuser': False,
                'is_staff': True,
                'group': 'profesor',
                'first_name': 'Carlos',
                'last_name': 'Tutor',
                'role': 'profesor',
            },
        ]

        for i in range(1, 21):
            users_data.append({
                'username': f'ID{i:05d}',
                'password': f'Estudiante2026!{i:02d}',
                'is_superuser': False,
                'is_staff': False,
                'group': 'estudiante',
                'first_name': 'Estudiante',
                'last_name': f'{i:02d}',
                'role': 'estudiante',
            })

        count = 0
        for data in users_data:
            user, created = User.objects.get_or_create(username=data['username'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = data['is_staff']
            user.is_superuser = data['is_superuser']
            user.set_password(data['password'])
            user.save()
            if data['group']:
                group = Group.objects.get(name=data['group'])
                user.groups.set([group])
            else:
                user.groups.clear()
            count += 1
            action = 'created' if created else 'updated'
            self.stdout.write(f"  [{data['role']}] {data['username']} — {action}")

        self.stdout.write(self.style.SUCCESS(f'\n✓ {count} users seeded successfully.'))

        if options['grades']:
            self._seed_grades()

    def _seed_grades(self):
        asignaturas = ['Matematicas', 'Lengua', 'Historia', 'Biologia', 'Fisica']
        Calificacion.objects.all().delete()
        for i in range(1, 21):
            Calificacion.objects.create(
                nombre_estudiante=f'Estudiante {i:02d}',
                identificacion=f'ID{i:05d}',
                asignatura=asignaturas[(i - 1) % len(asignaturas)],
                nota1=round(((i * 3) % 50) / 10, 1),
                nota2=round(((i * 7) % 50) / 10, 1),
                nota3=round(((i * 9) % 50) / 10, 1),
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {Calificacion.objects.count()} calificaciones seeded.'))
