# Documento de Prueba: Lector Markdown

¡Hola! Este es un documento Markdown renderizado de forma limpia y moderna para una lectura óptima sin etiquetas de sintaxis visibles como `#`, `**` o guiones.

---

## 🚀 Características del Visor

El visor convierte automáticamente la sintaxis Markdown en un documento estructurado y agradable para la lectura.

### 📝 Formatos de Texto y Tipografía
- Puedes leer texto en **negrita**, en *cursiva*, o incluso ~~tachado~~.
- Las citas en bloque tienen su propio estilo distinguido:

> "El diseño no es solo lo que se ve y lo que se siente. El diseño es cómo funciona."
> — Steve Jobs

### 🔔 Bloques de Notificación (Alerts)
> [!NOTE]
> Esta es una nota informativa para resaltar puntos clave del documento.

> [!TIP]
> Puedes presionar **Ctrl+E** o hacer clic en el botón **Editar (✏️)** en la barra de herramientas superior para editar este archivo.

> [!WARNING]
> Ten cuidado al modificar archivos críticos sin hacer una copia de seguridad.

---

## 📊 Tablas GFM (GitHub Flavored Markdown)

Las tablas se presentan organizadas con bordes limpios y encabezados destacados:

| Función | Atajo de Teclado | Descripción |
| :--- | :---: | :--- |
| **Abrir Archivo** | `Ctrl + O` | Abre un cuadro de diálogo para seleccionar otro archivo `.md` |
| **Editar Documento** | `Ctrl + E` | Conmuta a pantalla completa de edición con el botón de lápiz |
| **Guardar y Volver** | `Ctrl + S` | Guarda los cambios en disco y regresa a lectura limpia |
| **Alternar Tema** | Clic en Barra | Cambia entre Tema Claro (☀️) y Tema Oscuro (🌙) |
| **Buscar Texto** | `Ctrl + F` | Abre la barra de búsqueda rápida |
| **Zoom Texto** | `Ctrl + / Ctrl -` | Ajusta el tamaño de la fuente para leer cómodamente |

---

## ☑️ Listas de Tareas

- [x] Crear arquitectura limpia en Python y PyQt6.
- [x] Visor de lectura sin etiquetas de markdown visibles.
- [x] Botón de lápiz (✏️) para cambiar a modo edición.
- [x] Botón de guardar (💾) con guardado seguro en UTF-8.
- [x] Soporte para tema claro y tema oscuro con un clic.
- [x] Integración en el menú contextual del Explorador de Windows.
- [ ] Compilar ejecutable `.exe` independiente para distribución.

---

## 💻 Resaltado de Código

Los bloques de código incluyen resaltado sintáctico con tipografía monoespaciada:

```python
import sys

def saludar(nombre: str) -> str:
    """Función de ejemplo para probar el resaltado de sintaxis."""
    mensaje = f"¡Bienvenido a Lector Markdown, {nombre}!"
    print(mensaje)
    return mensaje

if __name__ == "__main__":
    saludar("Usuario de Windows")
```

También puedes visualizar bloques de código en otros lenguajes como JavaScript:

```javascript
function calcularTiempoLectura(totalPalabras) {
    const palabrasPorMinuto = 200;
    return Math.ceil(totalPalabras / palabrasPorMinuto);
}

console.log("Minutos estimados:", calcularTiempoLectura(650));
```

---

## 🔗 Enlaces y Navegación
- Puedes visitar la documentación de [Python](https://www.python.org/) o de [PyQt](https://riverbankcomputing.com/).
- Clic en cualquier enlace web para abrirlo en tu navegador predeterminado.
