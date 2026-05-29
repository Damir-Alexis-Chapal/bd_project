# Ajusta DB_HOST, DB_PORT, DB_SERVICE y las
# credenciales antes de ejecutar la aplicación.

# Conexión Oracle 
DB_HOST     = "localhost"
DB_PORT     = 1521
DB_SERVICE  = "FREE"       # o el nombre de tu servicio/SID
DB_USER     = "system"
DB_PASSWORD = "3578"

# DSN construido automáticamente
DB_DSN = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

# Aplicación 
APP_TITLE   = "Sistema Mundial de Fútbol 2026"
APP_WIDTH   = 1100
APP_HEIGHT  = 700

# Seguridad
# Número máximo de intentos de login fallidos
MAX_LOGIN_ATTEMPTS = 3