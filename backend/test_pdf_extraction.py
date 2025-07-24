#!/usr/bin/env python3
"""Test PDF extraction with different methods"""

import sys
import io
import PyPDF2
import pdfplumber
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available")

def test_pdf_extraction(pdf_path):
    """Test PDF extraction with all three methods"""
    
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()
    
    print(f"\n=== Testing PDF: {pdf_path} ===")
    print(f"File size: {len(pdf_content)} bytes")
    
    # Test PyMuPDF
    if PYMUPDF_AVAILABLE:
        print("\n--- Testing PyMuPDF ---")
        try:
            pdf_doc = fitz.open(pdf_path)
            print(f"Pages: {pdf_doc.page_count}")
            total_text = ""
            for i, page in enumerate(pdf_doc):
                text = page.get_text()
                print(f"Page {i+1}: {len(text)} characters")
                if text.strip():
                    print(f"  First 100 chars: {text[:100].strip()}")
                    total_text += text
            pdf_doc.close()
            print(f"Total extracted: {len(total_text)} characters")
        except Exception as e:
            print(f"PyMuPDF error: {e}")
    
    # Test pdfplumber
    print("\n--- Testing pdfplumber ---")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Pages: {len(pdf.pages)}")
            total_text = ""
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                print(f"Page {i+1}: {len(text)} characters")
                if text.strip():
                    print(f"  First 100 chars: {text[:100].strip()}")
                    total_text += text
            print(f"Total extracted: {len(total_text)} characters")
    except Exception as e:
        print(f"pdfplumber error: {e}")
    
    # Test PyPDF2
    print("\n--- Testing PyPDF2 ---")
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        print(f"Pages: {len(reader.pages)}")
        total_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"Page {i+1}: {len(text)} characters")
            if text.strip():
                print(f"  First 100 chars: {text[:100].strip()}")
                total_text += text
        print(f"Total extracted: {len(total_text)} characters")
    except Exception as e:
        print(f"PyPDF2 error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pdf_extraction.py <pdf_file>")
        sys.exit(1)
    
    test_pdf_extraction(sys.argv[1])