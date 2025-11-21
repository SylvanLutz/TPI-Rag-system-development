#!/usr/bin/env python3
"""
Export Mermaid diagrams from markdown files to PNG/SVG images.

This script extracts Mermaid diagram code blocks from markdown files and exports them
as PNG or SVG images for use in presentations, reports, and documentation.

Usage:
    python scripts/export_diagrams.py [--format png|svg] [--output-dir output/] [--file docs/ARCHITECTURE_DIAGRAM.md]
    
Requirements:
    - mermaid-cli: npm install -g @mermaid-js/mermaid-cli
    - Or use online export via mermaid.live
"""

import re
import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def extract_mermaid_diagrams(markdown_file: Path) -> List[Tuple[str, str, int]]:
    """
    Extract Mermaid diagram code blocks from markdown file.
    
    Args:
        markdown_file: Path to markdown file
        
    Returns:
        List of tuples: (diagram_name, diagram_code, line_number)
    """
    diagrams = []
    
    if not markdown_file.exists():
        logger.error(f"File not found: {markdown_file}")
        return diagrams
    
    content = markdown_file.read_text(encoding='utf-8')
    
    # Pattern to match mermaid code blocks
    pattern = r'```mermaid\n(.*?)```'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches, 1):
        diagram_code = match.group(1).strip()
        start_line = content[:match.start()].count('\n') + 1
        
        # Try to extract diagram name from preceding heading or comment
        before_match = content[:match.start()]
        heading_match = re.search(r'^###?\s+(.+)$', before_match, re.MULTILINE)
        if heading_match:
            diagram_name = heading_match.group(1).strip()
        else:
            diagram_name = f"diagram_{i}"
        
        # Clean diagram name for filename
        diagram_name = re.sub(r'[^\w\s-]', '', diagram_name)
        diagram_name = re.sub(r'[-\s]+', '_', diagram_name).lower()
        
        diagrams.append((diagram_name, diagram_code, start_line))
    
    return diagrams


def export_diagram_mermaid_cli(diagram_code: str, output_path: Path, format: str = 'png') -> bool:
    """
    Export diagram using mermaid-cli (mmdc).
    
    Args:
        diagram_code: Mermaid diagram code
        output_path: Output file path (without extension)
        format: 'png' or 'svg'
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create temporary .mmd file
        temp_mmd = output_path.with_suffix('.mmd')
        temp_mmd.write_text(diagram_code, encoding='utf-8')
        
        # Run mermaid-cli
        cmd = ['mmdc', '-i', str(temp_mmd), '-o', str(output_path.with_suffix(f'.{format}')), '-f', format]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up temp file
        temp_mmd.unlink()
        
        if result.returncode == 0:
            logger.info(f"✓ Exported: {output_path.with_suffix(f'.{format}')}")
            return True
        else:
            logger.error(f"✗ Failed to export {output_path.name}: {result.stderr}")
            return False
            
    except FileNotFoundError:
        logger.error("mermaid-cli (mmdc) not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        return False
    except Exception as e:
        logger.error(f"Error exporting diagram: {e}")
        return False


def export_diagram_instructions(diagram_code: str, output_path: Path, format: str = 'png') -> bool:
    """
    Generate instructions for manual export (when mermaid-cli not available).
    
    Args:
        diagram_code: Mermaid diagram code
        output_path: Output file path (without extension)
        format: 'png' or 'svg'
        
    Returns:
        True (always succeeds, just creates instruction file)
    """
    instruction_file = output_path.with_suffix('.export_instructions.txt')
    
    instructions = f"""Manual Export Instructions for {output_path.name}

Method 1: Online Export (Easiest)
1. Go to https://mermaid.live
2. Paste the diagram code below
3. Click "Actions" → "Download PNG" or "Download SVG"
4. Save as: {output_path.name}.{format}

Method 2: VS Code Extension
1. Install "Markdown Preview Mermaid Support" extension
2. Open the markdown file in VS Code
3. Right-click on the diagram → "Export as PNG/SVG"

Method 3: Install mermaid-cli
1. Install Node.js: https://nodejs.org/
2. Run: npm install -g @mermaid-js/mermaid-cli
3. Then re-run this script

Diagram Code:
---
{diagram_code}
---
"""
    
    instruction_file.write_text(instructions, encoding='utf-8')
    logger.info(f"📝 Created instructions: {instruction_file}")
    logger.info(f"   Visit https://mermaid.live to export manually")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Export Mermaid diagrams from markdown to PNG/SVG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export all diagrams from ARCHITECTURE_DIAGRAM.md as PNG
  python scripts/export_diagrams.py
  
  # Export as SVG
  python scripts/export_diagrams.py --format svg
  
  # Export from specific file
  python scripts/export_diagrams.py --file docs/DIAGRAM_OPTIMIZATION_AND_LINKAGE.md
  
  # Custom output directory
  python scripts/export_diagrams.py --output-dir exports/diagrams/
        """
    )
    
    parser.add_argument(
        '--file',
        type=Path,
        default=Path('docs/ARCHITECTURE_DIAGRAM.md'),
        help='Markdown file containing Mermaid diagrams (default: docs/ARCHITECTURE_DIAGRAM.md)'
    )
    
    parser.add_argument(
        '--format',
        choices=['png', 'svg'],
        default='png',
        help='Output format: png or svg (default: png)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('exports/diagrams'),
        help='Output directory for exported images (default: exports/diagrams)'
    )
    
    parser.add_argument(
        '--force-online',
        action='store_true',
        help='Skip mermaid-cli check and generate instruction files only'
    )
    
    args = parser.parse_args()
    
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Resolve file path
    if args.file.is_absolute():
        markdown_file = args.file
    else:
        markdown_file = project_root / args.file
    
    # Create output directory
    if args.output_dir.is_absolute():
        output_dir = args.output_dir
    else:
        output_dir = project_root / args.output_dir
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract diagrams
    logger.info(f"Reading diagrams from: {markdown_file}")
    diagrams = extract_mermaid_diagrams(markdown_file)
    
    if not diagrams:
        logger.warning("No Mermaid diagrams found in file")
        return 1
    
    logger.info(f"Found {len(diagrams)} diagram(s)")
    
    # Check if mermaid-cli is available
    has_mmdc = False
    if not args.force_online:
        try:
            result = subprocess.run(['mmdc', '--version'], capture_output=True, text=True)
            has_mmdc = result.returncode == 0
        except FileNotFoundError:
            has_mmdc = False
    
    if not has_mmdc and not args.force_online:
        logger.warning("mermaid-cli not found. Generating instruction files instead.")
        logger.info("Install with: npm install -g @mermaid-js/mermaid-cli")
        logger.info("Or use --force-online to skip this check")
    
    # Export each diagram
    success_count = 0
    for diagram_name, diagram_code, line_num in diagrams:
        output_path = output_dir / f"{markdown_file.stem}_{diagram_name}"
        
        logger.info(f"\nProcessing diagram '{diagram_name}' (line {line_num})...")
        
        if has_mmdc and not args.force_online:
            success = export_diagram_mermaid_cli(diagram_code, output_path, args.format)
            if success:
                success_count += 1
        else:
            # Generate instructions for manual export
            export_diagram_instructions(diagram_code, output_path, args.format)
            success_count += 1  # Count as success since instructions were created
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Export complete: {success_count}/{len(diagrams)} diagram(s) processed")
    logger.info(f"Output directory: {output_dir}")
    
    if not has_mmdc and not args.force_online:
        logger.info("\n💡 Tip: Install mermaid-cli for automatic export:")
        logger.info("   npm install -g @mermaid-js/mermaid-cli")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

