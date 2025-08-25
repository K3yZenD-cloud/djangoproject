# Django CRUD Application

Una aplicación web moderna construida con Django, lista para desplegar en Render.

## Características

- ✅ Django 5.2.5
- ✅ Interfaz moderna con Bootstrap 5
- ✅ Configuración para producción
- ✅ Listo para desplegar en Render
- ✅ Diseño responsive
- ✅ WhiteNoise para archivos estáticos

## Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd djangoproject
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   - Copia `.env.example` a `.env`
   - Configura las variables necesarias

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

## Despliegue en Render

1. **Conectar repositorio**
   - Sube tu código a GitHub
   - Conecta tu repositorio en Render

2. **Configurar servicio web**
   - Render detectará automáticamente el `render.yaml`
   - El build se ejecutará automáticamente

3. **Variables de entorno**
   - `SECRET_KEY`: Se genera automáticamente
   - `DEBUG`: Se establece en False para producción

## Estructura del Proyecto

```
djangoproject/
├── djangocrug/          # Configuración principal
│   ├── settings.py      # Configuraciones
│   ├── urls.py          # URLs principales
│   ├── wsgi.py          # WSGI para producción
│   └── asgi.py          # ASGI para async
├── main/                # Aplicación principal
│   ├── templates/       # Plantillas HTML
│   ├── views.py         # Vistas
│   ├── urls.py          # URLs de la app
│   └── models.py        # Modelos de datos
├── requirements.txt     # Dependencias
├── build.sh            # Script de construcción
├── render.yaml         # Configuración de Render
└── README.md           # Este archivo
```

## Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5, Font Awesome
- **Servidor**: Gunicorn
- **Archivos estáticos**: WhiteNoise
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
