# AWS Login Automation

Sencilla aplicación de escritorio para guardar credenciales de AWS y loguearse automáticamente en la consola usando Chrome.

Hecho con Python (CustomTkinter) y Selenium.

## Características
*   **Gestión de Cuentas**: Guarda múltiples cuentas (Alias, ID, Usuario, Contraseña).
*   **Login Automático**: Abre el navegador y rellena el formulario de login de AWS por ti.
*   **Seguridad**: Las contraseñas se guardan encriptadas en local (`accounts.json`) usando una clave generada en tu equipo.
*   **Interfaz**: Buscador integrado para filtrar cuentas rápidamente.

## Requisitos
*   Python 3.x
*   Google Chrome instalado

## Instalación y Uso

### Opción A: Ejecutable (Recomendado)
Entra en la carpeta **`dist/`** y ejecuta el archivo **`AWSLogin.exe`**.
¡Listo! No necesitas instalar Python ni configurar nada más.

### Opción B: Código Fuente
Si prefieres ejecutar el script manualmente:

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/kuoth00/IniciarSesionAWS.git
    cd IniciarSesionAWS
    ```

2.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar**:
    ```bash
    python main.py
    ```
    O simplemente doble click en `run_app.bat` (en Windows).

## Notas
*   **Importante**: No compartas nunca tu archivo `secret.key` ni `accounts.json`. El repositorio ya incluye un `.gitignore` para evitar subirlos por error.
