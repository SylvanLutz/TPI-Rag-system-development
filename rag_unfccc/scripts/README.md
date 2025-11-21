# Scripts Directory

Utility scripts for the TPI RAG system.

## Diagram Export Scripts

### `export_diagrams.py`

Python script to export Mermaid diagrams from markdown files to PNG/SVG images.

**⚠️ Setup Required**: See `EXPORT_SETUP.md` for installation instructions.

**Usage:**
```bash
# Export all diagrams from ARCHITECTURE_DIAGRAM.md as PNG
python scripts/export_diagrams.py

# Export as SVG
python scripts/export_diagrams.py --format svg

# Export from specific file
python scripts/export_diagrams.py --file docs/DIAGRAM_OPTIMIZATION_AND_LINKAGE.md

# Custom output directory
python scripts/export_diagrams.py --output-dir exports/diagrams/
```

**Requirements:**
- Python 3.7+
- Optional: `mermaid-cli` for automatic export (`npm install -g @mermaid-js/mermaid-cli`)
- If mermaid-cli is not installed, the script will generate instruction files for manual export

**Features:**
- Automatically extracts all Mermaid diagrams from markdown files
- Generates descriptive filenames based on diagram headings
- Creates instruction files if mermaid-cli is not available
- Supports both PNG and SVG export formats

### `export_diagrams.ps1`

PowerShell alternative for Windows users (basic functionality).

**Usage:**
```powershell
.\scripts\export_diagrams.ps1
```

**Note:** For full features, use the Python script instead.

## Database Scripts

### `run_sql_in_docker.ps1`

PowerShell script for Windows Docker networking workaround. See `docs/PROJECT_STRUCTURE.md` for details.

## Entity Management Scripts

### `sync_entities_to_db.py` (Planned)

Future script to sync entity management JSON files to database. See Issue #18 in `Issues_tracking/KNOWN_ISSUES.md`.

