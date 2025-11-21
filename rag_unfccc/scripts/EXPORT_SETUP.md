# Diagram Export Setup Guide

## Quick Start

The diagram export script needs `mermaid-cli` to automatically export diagrams. Here's how to set it up:

## Option 1: Install mermaid-cli (Recommended)

### Prerequisites
- **Node.js must be installed first** (npm comes bundled with Node.js)

### Step 1: Install Node.js (If Not Already Installed)

**Check if Node.js is installed:**
```powershell
node --version
```

**If you get an error** (like "node is not recognized"), you need to install Node.js:

1. **Download Node.js:**
   - Visit: https://nodejs.org/
   - Download the **LTS (Long Term Support)** version for Windows
   - This will install both Node.js and npm

2. **Run the installer:**
   - Run the downloaded `.msi` file
   - Follow the installation wizard (accept defaults)
   - **Important:** Make sure "Add to PATH" is checked during installation

3. **Restart your terminal:**
   - Close and reopen PowerShell/VS Code terminal
   - This ensures PATH changes take effect

4. **Verify installation:**
   ```powershell
   node --version    # Should show version like v20.x.x
   npm --version     # Should show version like 10.x.x
   ```

### Step 2: Install mermaid-cli

Once Node.js is installed, install mermaid-cli globally:
```powershell
npm install -g @mermaid-js/mermaid-cli
```

### Step 3: Verify mermaid-cli Installation

```powershell
mmdc --version
```
Should output something like: `@mermaid-js/mermaid-cli: 10.x.x`

### Step 4: Run the Export Script

Now you can run the export script:
   ```powershell
   python scripts/export_diagrams.py
   ```

**Export as SVG instead of PNG:**
```powershell
python scripts/export_diagrams.py --format svg
```

### Troubleshooting

**If `npm` is not recognized:**
- Make sure Node.js is installed and added to PATH
- Restart your terminal after installing Node.js
- Try: `node --version` to verify Node.js is installed

**If `mmdc` command not found after installation:**
- Check npm global bin path: `npm config get prefix`
- Add that path to your system PATH environment variable
- Or use: `npx @mermaid-js/mermaid-cli` instead of `mmdc`

## Option 2: Manual Export (No Installation Required)

If you don't want to install Node.js, you can export diagrams manually:

1. **Run the script to generate instruction files:**
   ```powershell
   python scripts/export_diagrams.py
   ```

2. **Open the instruction files:**
   - Located in: `exports/diagrams/*.export_instructions.txt`
   - Each file contains the diagram code and export instructions

3. **Export manually:**
   - Go to https://mermaid.live
   - Paste the diagram code from the instruction file
   - Click "Actions" → "Download PNG" or "Download SVG"
   - Save the file with the suggested filename

## Option 3: Use VS Code Extension

1. **Install extension:**
   - Open VS Code
   - Install "Markdown Preview Mermaid Support" extension

2. **Export from markdown:**
   - Open `docs/ARCHITECTURE_DIAGRAM.md` in VS Code
   - Right-click on any Mermaid diagram
   - Select "Export as PNG" or "Export as SVG"

## Script Options

```powershell
# Export all diagrams as PNG (default)
python scripts/export_diagrams.py

# Export as SVG
python scripts/export_diagrams.py --format svg

# Export from specific file
python scripts/export_diagrams.py --file docs/DIAGRAM_OPTIMIZATION_AND_LINKAGE.md

# Custom output directory
python scripts/export_diagrams.py --output-dir my_exports/

# Force online mode (skip mermaid-cli check, generate instructions only)
python scripts/export_diagrams.py --force-online
```

## Output Location

- **Default**: `exports/diagrams/`
- **Format**: `{filename}_{diagram_name}.{png|svg}`
- **Example**: `ARCHITECTURE_DIAGRAM_1_current_state_refactored_system_architecture.png`

## What the Script Does

1. **Extracts diagrams** from markdown files (finds all ````mermaid` code blocks)
2. **Names diagrams** based on headings (e.g., "Current State: Refactored System Architecture")
3. **Exports to images** using mermaid-cli (if installed) or generates instruction files
4. **Organizes output** in a structured directory

## Need Help?

- Check `scripts/README.md` for general script documentation
- See `docs/DIAGRAM_OPTIMIZATION_AND_LINKAGE.md` for diagram optimization strategies
- Open an issue if you encounter problems

