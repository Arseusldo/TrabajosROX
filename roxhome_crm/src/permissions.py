ROLE_PAGES = {
    'Administrador': {'*'},
    'Dirección': {'*'},
    'Coordinación': {'Inicio','Posibles clientes','Contactos','Cuentas','Tratos','Facturas','Servicios técnicos','Técnicos','Tareas','Informes','Análisis'},
    'Ventas': {'Inicio','Posibles clientes','Contactos','Cuentas','Tratos','Presupuestos','Llamadas','Tareas'},
    'Técnico': {'Inicio','Servicios técnicos','Checklists','Evidencias','Horarios'},
    'Marketing': {'Inicio','Campañas','Social','Informes'},
    'Solo lectura': {'Inicio','Informes','Análisis'}
}

def can_access(role, page):
    allowed = ROLE_PAGES.get(role, set())
    return '*' in allowed or page in allowed
