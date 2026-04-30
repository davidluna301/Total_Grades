def role_context(request):
    user = request.user

    if not user.is_authenticated:
        return {
            'current_role': None,
            'is_superadmin': False,
            'is_profesor': False,
            'is_estudiante': False,
        }

    is_superadmin = user.is_superuser
    is_profesor = user.groups.filter(name='profesor').exists()
    is_estudiante = user.groups.filter(name='estudiante').exists()

    current_role = None
    if is_superadmin:
        current_role = 'superadmin'
    elif is_profesor:
        current_role = 'profesor'
    elif is_estudiante:
        current_role = 'estudiante'

    return {
        'current_role': current_role,
        'is_superadmin': is_superadmin,
        'is_profesor': is_profesor,
        'is_estudiante': is_estudiante,
    }