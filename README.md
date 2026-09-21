# 📖 Lector Markdown (Windows Desktop)

Aplicación de escritorio moderna y rápida desarrollada en Python con PyQt6 para leer y editar archivos Markdown (`.md`) en Windows.

Abre tus archivos Markdown convertidos al instante en una **lectura limpia, estética y agradable sin etiquetas de sintaxis visibles** (sin `#`, `**`, `*`, `~~`, etc.). Y cuando necesites hacer modificaciones, basta con pulsar el botón de **lápiz (✏️)** para editar el archivo original en pantalla completa y guardarlo (`Ctrl+S`).

---

## 🚀 Características Principales

- **Visor de Lectura Enriquecida:**
  - Renderizado automático sin etiquetas Markdown a la vista.
  - Tipografía moderna estilo GitHub / Typora con espaciado optimizado.
  - Soporte completo para tablas GFM con bordes limpios.
  - Listas de tareas interactivas con casillas de verificación (☑ / ☐).
  - Bloques de código con resaltado sintáctico inteligente (Pygments).
  - Citas en bloque y avisos especiales estilo GitHub (`[!NOTE]`, `[!TIP]`, `[!WARNING]`, etc.).
  - Enlaces web clicables que abren directamente en tu navegador.

- **Modo Edición Rápida (Botón Lápiz ✏️):**
  - Conmutador fluido entre Modo Lectura y Modo Edición a pantalla completa.
  - Editor con numeración de líneas y sangría inteligente de 4 espacios (Tab y Shift+Tab).
  - Botón **Guardar (💾)** y atajo `Ctrl+S` que guarda los cambios en el archivo `.md` y regresa de inmediato al modo lectura actualizado.
  - Notificación de seguridad si intentas salir o cambiar de vista con cambios sin guardar.

- **Diseño y Temas:**
  - Selector instantáneo de **Tema Claro** (☀️) y **Tema Oscuro** (🌙) en la barra de herramientas.
  - Control de Zoom (`Ctrl +`, `Ctrl -`, o `Ctrl + Rueda del ratón`).
  - Barra de búsqueda integrada (`Ctrl+F`) con búsqueda hacia adelante y atrás (`F3` / `Shift+F3`).

- **Integración Nativa en Windows:**
  - Menú contextual en el Explorador de Windows: Clic derecho en cualquier archivo `.md` ➔ **"Abrir con Lector Markdown"**.
  - Asociación predeterminada para que el doble clic sobre archivos `.md` los abra directamente con la aplicación.
  - Diálogo dentro de la app para activar o desinstalar la integración con 1 solo clic.
  - Soporta arrastrar y soltar (Drag and Drop) archivos `.md` directamente sobre la ventana.

---

## 📂 Estructura del Proyecto

```
LectorMarkdown/
│
├── main.py                     # Punto de entrada principal (acepta sys.argv[1] desde Windows)
├── config.py                   # Persistencia de configuración (temas, historial, geometría)
├── sample.md                   # Documento de prueba con ejemplos de sintaxis
├── build_exe.py               # Script de compilación a .exe independiente
├── requirements.txt           # Dependencias de Python
│
├── core/
│   ├── markdown_parser.py     # Motor de renderizado Markdown a HTML con resaltado
│   ├── file_manager.py        # Carga, guardado seguro en UTF-8 y estadísticas
│   └── windows_registry.py    # Integración con el Registro de Windows (HKCU)
│
├── ui/
│   ├── main_window.py         # Ventana principal, barra de herramientas y flujo de estados
│   ├── reader_view.py         # Visor de lectura limpia basado en QTextBrowser
│   ├── editor_view.py         # Editor de texto plano con numeración de líneas
│   ├── search_bar.py          # Barra de búsqueda en el documento (Ctrl+F)
│   ├── styles.py              # Hojas de estilo CSS (lector) y QSS (interfaz)
│   └── resources.py           # Iconos vectoriales de alta resolución
│
├── assets/
│   ├── icon.ico               # Icono de la aplicación para Windows
│   └── icon.png               # Icono en alta resolución
│
├── scripts/
│   ├── registrar_windows.bat  # Script para activar el menú contextual y asociación .md
│   └── eliminar_windows.bat   # Script para desinstalar la integración del registro
│
└── tests/
    └── test_lector.py         # Pruebas unitarias automatizadas
```

---

## 🛠️ Instalación y Uso con Python

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
Para abrir la aplicación directamente:
```bash
python main.py
```
O abrir un archivo markdown específico:
```bash
python main.py sample.md
```

Para abrir sin ventana de consola negra en Windows:
```bash
pythonw main.py sample.md
```

---

## 📦 Compilación a Ejecutable Nativo (.exe)

Para generar el ejecutable autónomo para Windows (`dist\LectorMarkdown.exe`):

```bash
python build_exe.py
```

El ejecutable resultante:
- No requiere que el usuario final tenga Python instalado.
- No muestra ninguna ventana de consola negra (`--noconsole`).
- Tiene el icono personalizado incrustado.
- Se puede copiar a cualquier carpeta de tu equipo.

---

## 🪟 Cómo Activar la Opción "Abrir con..." en Windows

Tienes **dos formas sencillas** de activar la integración:

### Opción A (Desde la propia aplicación):
1. Abre Lector Markdown.
2. En la barra superior, haz clic en el botón **"Integración Windows"** (icono de Windows ⚙️).
3. Haz clic en **"Activar Integración"**. ¡Listo!

### Opción B (Con script automático):
1. Haz doble clic sobre el archivo `scripts\registrar_windows.bat`.

> **Nota:** La integración se guarda en `HKEY_CURRENT_USER\Software\Classes`, por lo que **no requiere permisos de Administrador** y no afecta a otros usuarios de la máquina.

Para desinstalar la integración en cualquier momento, usa el botón "Desinstalar Integración" dentro de la app o ejecuta `scripts\eliminar_windows.bat`.

---

## ⌨️ Atajos de Teclado

| Atajo | Acción |
| :--- | :--- |
| `Ctrl + O` | Abrir un nuevo archivo Markdown |
| `Ctrl + E` | Cambiar a modo **Edición (✏️)** |
| `Ctrl + S` | **Guardar cambios (💾)** y volver a la vista de lectura |
| `Ctrl + F` | Mostrar/Ocultar barra de búsqueda |
| `F3` / `Enter` | Siguiente coincidencia en la búsqueda |
| `Shift + F3` | Coincidencia anterior en la búsqueda |
| `Esc` | Cerrar búsqueda o volver al modo de lectura |
| `Ctrl + +` / `Ctrl + -` | Aumentar / Disminuir tamaño de fuente (Zoom) |
| `Ctrl + Rueda del ratón` | Zoom interactivo con la rueda del ratón |
| `Tab` / `Shift + Tab` | Indentar / Desindentar 4 espacios en el editor |
