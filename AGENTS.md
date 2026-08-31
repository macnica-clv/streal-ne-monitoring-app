# AGENTS.md

## Project
Hiz-mil is a Python 3.12 / PySide6 desktop application for SR300 and SR500 monitoring units.

## Structure
- `Controllers/`: GUI and headless application flow.
- `Models/`: device drivers, config, sensor, and register models.
- `Views/`: hand-written view wrappers and generated Qt UI Python files.
- `UI/`: Qt Designer `.ui` source files.
- `Views/qml/`: QML components.
- `qss/`: theme stylesheets.
- `Utils/`: app control, resource loading, and helper utilities.

## Editing Rules
- Do not edit generated files directly:
  - `Views/UI/*.py`
  - `Views/*_Page.py`
  - `Views/resources_rc.py`
- Prefer changing source files:
  - `Controllers/*.py`
  - `Models/*.py`
  - `Views/*View.py`
  - `UI/*.ui`
  - `Views/qml/*.qml`
  - `qss/*.qss`
- Preserve both SR300 and SR500 behavior unless the task explicitly targets one model.
- Do not require real hardware for verification unless the user says hardware is available.
- Keep changes scoped to the requested behavior and avoid unrelated refactors.

## Maintaining This File
- Update `AGENTS.md` when a task reveals stable project knowledge that will help future Codex sessions.
- Good additions include recurring verification commands, generated-file rules, setup requirements, architecture conventions, and hardware/test limitations.
- Do not add task-specific notes, temporary debugging observations, or details likely to become stale quickly.
- Keep this file concise. Prefer updating an existing section over adding a new one.
- If an `AGENTS.md` update seems useful but uncertain, mention it in the final response instead of editing it.

## Run
The reference development environment at Macnica is PyCharm + Miniforge3 (conda).
`environment.yml` targets the conda-forge channel.

Create the full GUI environment with conda:

```powershell
conda env create -f environment.yml
conda activate Hiz-mil
```

Or with venv + pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Dependency files: `requirements.txt` (GUI), `requirements-headless.txt` (headless,
pyserial only), `requirements-build.txt` (PyInstaller). Keep them ASCII-only:
pip decodes requirements files with the locale encoding on Windows, so non-ASCII
comments break installation under cp932.

Run the GUI app:

```powershell
python main.py
```

Run the headless app:

```powershell
python main.py --headless
```

## Verification
Run this after Python changes when relevant:

```powershell
python -m compileall Controllers Models Utils Views main.py main_headless.py
```

Headless smoke check (requires `python main.py --headless` running in another
terminal; this command is a client of the app control server):

```powershell
python -c "from Utils.AppControl import ping, get_app_status; print(ping()); print(get_app_status())"
```
