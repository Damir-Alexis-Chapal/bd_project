# Roles de usuario 
ROLE_ADMIN       = "Admin"
ROLE_TRADICIONAL = "Tradicional"
ROLE_ESPORADICO  = "Esporadico"

ALL_ROLES = [ROLE_ADMIN, ROLE_TRADICIONAL, ROLE_ESPORADICO]

# Permisos por rol
# Qué acciones puede realizar cada rol
PERMISOS = {
    ROLE_ADMIN: {
        "crear_usuarios": True,
        "crud":           True,
        "consultas":      True,
        "reportes":       True,
        "bitacora":       True,
    },
    ROLE_TRADICIONAL: {
        "crear_usuarios": False,
        "crud":           True,
        "consultas":      True,
        "reportes":       True,
        "bitacora":       False,
    },
    ROLE_ESPORADICO: {
        "crear_usuarios": False,
        "crud":           False,
        "consultas":      True,
        "reportes":       True,
        "bitacora":       False,
    },
}

# Países anfitriones
PAISES_ANFITRIONES = ["México", "USA", "Canadá"]

# Colores de la UI
COLOR_PRIMARY    = "#1a3a5c"   # Azul oscuro (barra superior)
COLOR_SECONDARY  = "#2e6da4"   # Azul medio (botones principales)
COLOR_ACCENT     = "#e8f0fe"   # Azul claro (fondos de formulario)
COLOR_SUCCESS    = "#2e7d32"   # Verd
COLOR_DANGER     = "#c62828"   # Rojo
COLOR_BG         = "#f5f5f5"   # Fondo general
COLOR_TEXT       = "#212121"   # Texto principal
COLOR_TEXT_LIGHT = "#ffffff"   # Texto sobre fondo oscuro