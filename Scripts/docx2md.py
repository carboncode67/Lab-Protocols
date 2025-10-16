#!/usr/bin/env python3
"""
Convert Word documents to clean Markdown suitable for MkDocs.

This script:
1. Uses pandoc to convert DOCX to markdown with extracted media
2. Cleans up image references (removes width/height attributes)
3. Converts underlined text patterns to proper markdown headers
4. Removes "AI-generated content may be incorrect" from alt text
5. Ensures proper asset paths
"""

import subprocess
import re
import os
import shutil
from pathlib import Path
docx_path = r"C:\Users\twk54\Desktop\Projects\Protocols\Lab-Protocols\docs\Protocol_Maize Whole Plant Processing.docx"
output_dir = r"C:\Users\twk54\Desktop\Projects\Protocols\Lab-Protocols\docs"



def convert_docx_to_markdown(docx_path, output_dir=None, assets_folder="assets"):
    """
    Convert a DOCX file to clean markdown with extracted images.
    
    Args:
        docx_path: Path to the Word document
        output_dir: Output directory (defaults to same as input file)
        assets_folder: Name of the folder for images (default: "assets")
    
    Returns:
        Path to the created markdown file
    """
    docx_path = Path(docx_path)
    
    if not docx_path.exists():
        raise FileNotFoundError(f"Document not found: {docx_path}")
    
    # Set output directory
    if output_dir is None:
        output_dir = docx_path.parent
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create temp directory for pandoc
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    # Create temporary markdown file
    temp_md = temp_dir / f"{docx_path.stem}.md"
    final_md = output_dir / f"{docx_path.stem}.md"
    
    # Document-specific subfolder in assets (using doc name without spaces)
    doc_name = docx_path.stem.replace(' ', '_').lower()
    assets_subdir = output_dir / assets_folder / doc_name
    
    # Run pandoc with extract-media to temp folder
    print(f"Converting {docx_path.name} with pandoc...")
    try:
        subprocess.run(
            [
                "pandoc",
                str(docx_path),
                "-o", str(temp_md),
                "--extract-media", str(temp_dir),  # Pandoc will create temp/media
                "-t", "markdown"
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ Pandoc conversion complete")
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e.stderr}")
        raise
    
    # Read the converted markdown
    with open(temp_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Path for images in markdown (relative to the .md file)
    relative_image_path = f"{assets_folder}/{doc_name}"
    
    # Clean up the content with the correct image path
    content = clean_markdown(content, relative_image_path)
    
    # Write cleaned markdown
    with open(final_md, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Move images from temp/media to assets/doc_name
    temp_media_dir = temp_dir / "media"
    
    if temp_media_dir.exists():
        print(f"Moving images to {relative_image_path}/...")
        
        # Create assets directory structure
        assets_subdir.mkdir(parents=True, exist_ok=True)
        
        # Move all images
        image_count = 0
        for image_file in temp_media_dir.iterdir():
            if image_file.is_file():
                dest = assets_subdir / image_file.name
                shutil.move(str(image_file), str(dest))
                image_count += 1
        
        print(f"✓ Moved {image_count} images to {relative_image_path}/")
    
    # Clean up temp directory
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print("✓ Cleaned up temporary files")
    
    print(f"\n✓ Conversion complete!")
    print(f"  Markdown file: {final_md}")
    print(f"  Images folder: {assets_subdir}")
    
    return final_md


def clean_markdown(content, image_path):
    """
    Clean up markdown content from pandoc conversion.
    
    Args:
        content: Raw markdown content
        image_path: Path for image references (e.g., "assets/doc_name")
    
    Returns:
        Cleaned markdown content
    """
    
    # 1. First, consolidate any image markdown that spans multiple lines
    # This handles cases where pandoc/Word adds line breaks within the image syntax
    # Pattern matches: ![...](...)  or  ![...](...){...} even with newlines
    def consolidate_image_lines(match):
        # Get the entire match and remove all internal newlines
        full_match = match.group(0)
        # Replace newlines with spaces, then clean up multiple spaces
        consolidated = re.sub(r'\s+', ' ', full_match)
        return consolidated
    
    # Match image syntax across multiple lines (DOTALL flag makes . match newlines)
    content = re.sub(
        r'!\[[^\]]*\]\([^)]+\)(?:\{[^}]*\})?',
        consolidate_image_lines,
        content,
        flags=re.DOTALL
    )
    
    # 2. Fix image references - remove width/height and clean alt text
    # Pattern: ![alt text](path){width="..." height="..."}
    def fix_image_ref(match):
        alt_text = match.group(1)
        original_path = match.group(2)
        
        # Clean alt text - remove "AI-generated content may be incorrect"
        # Handle various forms: with/without period, with/without extra spaces
        alt_text = re.sub(r'\s*AI-generated content may be incorrect\.?\s*', '', alt_text, flags=re.IGNORECASE)
        # Also remove any remaining multiple spaces
        alt_text = re.sub(r'\s+', ' ', alt_text)
        alt_text = alt_text.strip()
        
        # Extract just the filename from the original path
        filename = Path(original_path).name
        
        # Create new path
        new_path = f'{image_path}/{filename}'
        
        return f'![{alt_text}]({new_path})'
    
    content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)\{[^}]*\}',
        fix_image_ref,
        content
    )
    
    # 3. Also handle images without the curly braces
    def fix_simple_image(match):
        alt_text = match.group(1)
        original_path = match.group(2)
        
        # Clean alt text - remove "AI-generated content may be incorrect"
        alt_text = re.sub(r'\s*AI-generated content may be incorrect\.?\s*', '', alt_text, flags=re.IGNORECASE)
        alt_text = re.sub(r'\s+', ' ', alt_text)
        alt_text = alt_text.strip()
        
        # Extract just the filename
        filename = Path(original_path).name
        
        # Create new path
        new_path = f'{image_path}/{filename}'
        
        return f'![{alt_text}]({new_path})'
    
    content = re.sub(
        r'!\[([^\]]*)\]\(((?:-s/)?media/[^)]+)\)',
        fix_simple_image,
        content
    )
    
    # 2. Convert [Text]{.underline}: patterns to markdown headers
    # These are typically section headers that should be ## headings
    def convert_underlined_headers(match):
        text = match.group(1)
        # Remove the trailing colon if present
        text = text.rstrip(':')
        return f'\n## {text}\n'
    
    content = re.sub(
        r'\[([^\]]+)\]\{\.underline\}:?',
        convert_underlined_headers,
        content
    )
    
    # 3. Remove blockquote markers (>) from the beginning if the whole doc is quoted
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove leading "> " but preserve other content
        if line.startswith('> '):
            cleaned_lines.append(line[2:])
        elif line.startswith('>') and len(line) == 1:
            cleaned_lines.append('')
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # 4. Add a proper title if not present
    if not content.lstrip().startswith('#'):
        # Try to extract a title from the first meaningful line
        first_line = content.lstrip().split('\n')[0]
        if first_line and len(first_line) < 100:
            # Use first line as title if reasonable
            content = f"# {first_line}\n\n" + '\n'.join(content.lstrip().split('\n')[1:])
    
    # 5. Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 6. Fix specific formatting issues
    # Replace escaped arrows in text
    content = content.replace('-\\>', '->')
    content = content.replace('\\<-', '<-')
    
    # 7. Clean up any remaining blockquote artifacts in lists
    content = re.sub(r'^  > ', '  ', content, flags=re.MULTILINE)
    
    return content.strip() + '\n'


if __name__ == "__main__":
    # Hardcoded path for now

    
    # Images will be organized as: assets/document_name/image1.jpg, image2.jpg, etc.
    # This prevents conflicts when processing multiple documents
    
    # You can also specify custom output directory and assets folder name
    # output_dir = "/path/to/output"
    # assets_folder = "images"
    
    try:
        result = convert_docx_to_markdown(
            docx_path,
            output_dir=output_dir,  # Uncomment to use custom output dir
            assets_folder="assets"
        )
        print(f"\n✅ Success! Markdown file ready at:\n   {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()