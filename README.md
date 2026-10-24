# Task Manager

Aplicación de consola para crear y administrar tareas. Las tareas se guardan en
`tasks.json` para conservarlas entre ejecuciones.

## Requisitos

- Python 3.10 o posterior (el menú utiliza `match/case`).

## Instalación

Desde la raíz del proyecto, crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo según tu sistema:

```bash
# Linux o macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Con el entorno virtual activado, instala las dependencias listadas en
`requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Para salir del entorno virtual cuando termines, ejecuta `deactivate`. Si
prefieres no usar un entorno virtual, puedes ejecutar los comandos de
instalación con el Python de tu sistema, aunque se recomienda mantener las
dependencias del proyecto aisladas.

## Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
python main.py
```

El menú permite:

1. Añadir una tarea con nombre y descripción.
2. Eliminar una tarea por su identificador.
3. Mostrar las tareas y su estado (pendiente o completada).
4. Marcar una tarea como completada.
5. Salir.

Los datos se leen de `tasks.json` al iniciar y se guardan después de añadir,
eliminar o completar una tarea. Si el archivo no existe, la aplicación empieza
con una lista vacía. La ruta es relativa al directorio desde el que se ejecuta
`main.py`.

## Estructura

```text
.
├── ai_service/
│   └── open_ai_service.py
├── task_manager/
│   ├── Task.py
│   └── TaskManager.py
├── tests/
│   └── test_task_manager.py
├── main.py
└── tasks.json
```

- `task_manager/Task.py`: modelo de una tarea, con identificador, nombre,
  descripción y estado de finalización.
- `task_manager/TaskManager.py`: operaciones para añadir, eliminar, listar y
  completar tareas, además de cargar y guardar los datos JSON.
- `main.py`: interfaz de consola.
- `ai_service/open_ai_service.py`: función opcional `create_task_with_ai` que
  solicita a OpenAI una respuesta basada en el nombre y la descripción. No está
  conectada al menú principal.
- `tests/test_task_manager.py`: pruebas unitarias del gestor de tareas.

## Servicio opcional de IA

Las dependencias `openai` y `python-dotenv` están incluidas en
`requirements.txt`. Configura la variable `OPEN_API_KEY` en el entorno antes
de ejecutar código que use `ai_service/open_ai_service.py`. El módulo carga
variables desde `.env` con `python-dotenv`; no guardes claves reales en el
repositorio. Este servicio es opcional y no está conectado al menú principal.

## Pruebas

Desde la raíz del proyecto:

```bash
python -m unittest discover -s tests -v
```

Las pruebas usan directorios temporales para los archivos JSON, por lo que no
modifican el `tasks.json` de la aplicación.
