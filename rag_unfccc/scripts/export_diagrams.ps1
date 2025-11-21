# PowerShell script to export Mermaid diagrams from markdown files
# Alternative to Python script for Windows users

param(
    [string]$File = "docs/ARCHITECTURE_DIAGRAM.md",
    [ValidateSet("png", "svg")]
    [string]$Format = "png",
    [string]$OutputDir = "exports/diagrams"
)

Write-Host "Mermaid Diagram Export Script (PowerShell)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check if mermaid-cli is installed
try {
    $mmdcVersion = mmdc --version 2>&1
    Write-Host "✓ mermaid-cli found" -ForegroundColor Green
} catch {
    Write-Host "✗ mermaid-cli not found. Installing..." -ForegroundColor Yellow
    npm install -g @mermaid-js/mermaid-cli
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install mermaid-cli" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ mermaid-cli installed" -ForegroundColor Green
}

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "✓ Created output directory: $OutputDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "Note: This PowerShell script provides basic functionality." -ForegroundColor Yellow
Write-Host "For full features (diagram extraction, naming, etc.), use:" -ForegroundColor Yellow
Write-Host "  python scripts/export_diagrams.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "For manual export, visit: https://mermaid.live" -ForegroundColor Cyan
Write-Host ""

exit 0

