import os
from pathlib import Path

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluaciones_total_grades_estudiantes.settings')
django.setup()

from django.contrib.auth.models import Group, User


ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / 'usuarios_y_contrasenas.txt'


def create_or_update_user(username, password, *, is_superuser=False, is_staff=False, group_name=None, first_name='', last_name=''):
    user, created = User.objects.get_or_create(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.is_staff = is_staff or is_superuser
    user.is_superuser = is_superuser
    user.set_password(password)
    user.save()

    if group_name:
        group = Group.objects.get(name=group_name)
        user.groups.set([group])
    else:
        user.groups.clear()

    return user, created


def main():
    Group.objects.get_or_create(name='profesor')
    Group.objects.get_or_create(name='estudiante')

    credentials = []

    users_to_create = [
        {
            'username': 'superadmin',
            'password': 'SuperAdmin2026!',
            'is_superuser': True,
            'is_staff': True,
            'group_name': None,
            'first_name': 'Super',
            'last_name': 'Admin',
            'role': 'superadmin',
        },
        {
            'username': 'profesor1',
            'password': 'Profesor2026!',
            'is_superuser': False,
            'is_staff': True,
            'group_name': 'profesor',
            'first_name': 'Laura',
            'last_name': 'Docente',
            'role': 'profesor',
        },
        {
            'username': 'profesor2',
            'password': 'Profesor2026!',
            'is_superuser': False,
            'is_staff': True,
            'group_name': 'profesor',
            'first_name': 'Carlos',
            'last_name': 'Tutor',
            'role': 'profesor',
        },
    ]

    for index in range(1, 21):
        users_to_create.append(
            {
                'username': f'ID{index:05d}',
                'password': f'Estudiante2026!{index:02d}',
                'is_superuser': False,
                'is_staff': False,
                'group_name': 'estudiante',
                'first_name': 'Estudiante',
                'last_name': f'{index:02d}',
                'role': 'estudiante',
            }
        )

    for user_data in users_to_create:
        user, _ = create_or_update_user(
            user_data['username'],
            user_data['password'],
            is_superuser=user_data['is_superuser'],
            is_staff=user_data['is_staff'],
            group_name=user_data['group_name'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
        credentials.append(
            f"Rol: {user_data['role']} | Usuario: {user.username} | Contrasena: {user_data['password']}"
        )

    OUTPUT_FILE.write_text('\n'.join(credentials), encoding='utf-8')
    print(f'created_or_updated_users={len(credentials)}')
    print(f'credentials_file={OUTPUT_FILE}')


if __name__ == '__main__':
    main()