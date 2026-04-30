import os

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluaciones_total_grades_estudiantes.settings')
django.setup()

from calificaciones_total_grades_estudiantes.models import Calificacion


def main():
    asignaturas = ['Matematicas', 'Lengua', 'Historia', 'Biologia', 'Fisica']

    Calificacion.objects.all().delete()

    for index in range(1, 21):
        Calificacion.objects.create(
            nombre_estudiante=f'Estudiante {index:02d}',
            identificacion=f'ID{index:05d}',
            asignatura=asignaturas[(index - 1) % len(asignaturas)],
            nota1=((index * 3) % 50) / 10,
            nota2=((index * 7) % 50) / 10,
            nota3=((index * 9) % 50) / 10,
        )

    print(f'created_records={Calificacion.objects.count()}')


if __name__ == '__main__':
    main()