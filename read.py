#!/usr/bin/env python3
"""
Markdown to PDF Converter Script
Converts README.md file to a formatted PDF document
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import argparse
import sys

def convert_md_to_pdf(input_file='README.md', output_file='README.pdf'):
    """
    Convert a Markdown file to PDF with proper formatting
    
    Args:
        input_file (str): Path to the input markdown file
        output_file (str): Path to the output PDF file
    """
    
    try:
        # Read the markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML with extensions for better formatting
        html = markdown.markdown(
            md_content,
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.codehilite',
                'markdown.extensions.fenced_code',
                'markdown.extensions.toc'
            ]
        )
        
        # CSS styles for better PDF formatting
        css_styles = """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 24pt;
            margin-top: 20px;
        }
        
        h2 {
            color: #34495e;
            font-size: 18pt;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        h3 {
            color: #7f8c8d;
            font-size: 14pt;
            margin-top: 15px;
            margin-bottom: 8px;
        }
        
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.4;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        ul, ol {
            margin-left: 20px;
            margin-bottom: 10px;
        }
        
        li {
            margin-bottom: 5px;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 10px 0;
            padding-left: 15px;
            color: #7f8c8d;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        /* Fix for tree structure display */
        pre:contains("├──"), pre:contains("└──") {
            font-family: 'Courier New', monospace;
            white-space: pre;
        }
        """
        
        # Create complete HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>README - analytING</title>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(
            output_file,
            stylesheets=[CSS(string=css_styles)]
        )
        
        print(f"✅ Successfully converted {input_file} to {output_file}")
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        return False

def install_dependencies():
    """
    Install required dependencies
    """
    print("Installing required dependencies...")
    import subprocess
    
    dependencies = [
        'markdown',
        'weasyprint'
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
            return False
    
    return True

def main():
    """
    Main function to handle command line arguments and execute conversion
    """
    parser = argparse.ArgumentParser(description='Convert Markdown file to PDF')
    parser.add_argument(
        '-i', '--input', 
        default='README.md',
        help='Input markdown file (default: README.md)'
    )
    parser.add_argument(
        '-o', '--output',
        default='README.pdf', 
        help='Output PDF file (default: README.pdf)'
    )
    parser.add_argument(
        '--install-deps',
        action='store_true',
        help='Install required dependencies'
    )
    
    args = parser.parse_args()
    
    if args.install_deps:
        if not install_dependencies():
            print("Failed to install dependencies. Please install manually:")
            print("pip install markdown weasyprint")
            return 1
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"❌ Input file '{args.input}' does not exist.")
        return 1
    
    # Convert the file
    success = convert_md_to_pdf(args.input, args.output)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())