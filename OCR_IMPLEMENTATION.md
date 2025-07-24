# OCR Implementation for Scanned PDFs

## Problem
スキャンされたPDF（画像ベースのPDF）からテキストを抽出できない問題

## Solution
Gemini Vision APIを使用したOCR実装

### Implementation Details

1. **PDF Analysis**:
   - PyMuPDF detects blocks and images on each page
   - If blocks=1 and images=1, it's likely a scanned PDF

2. **OCR Process**:
   - Extract images from PDF pages using PyMuPDF
   - Send each page image to Gemini Vision API
   - Gemini performs OCR with Japanese language understanding
   - Combine text from all pages

3. **Fallback Strategy**:
   ```
   1. PyMuPDF (text extraction)
   2. pdfplumber (text extraction)
   3. PyPDF2 (text extraction)
   4. OCR with Gemini Vision (for scanned PDFs)
   ```

### Key Features

- **Japanese Support**: Gemini Vision API has excellent Japanese OCR capabilities
- **No Additional Setup**: Uses existing Gemini API key
- **High Accuracy**: Gemini understands context and formatting
- **Automatic Detection**: OCR activates only when regular extraction fails

### Usage

The OCR process is automatic. When you upload a scanned PDF:
1. Regular text extraction methods are tried first
2. If no text is found, OCR is automatically triggered
3. The extracted text is then sent to Gemini for career analysis

### Limitations

1. **Processing Time**: OCR takes longer than regular text extraction
2. **API Costs**: Each page requires a Gemini API call
3. **Image Quality**: Low-quality scans may produce poor results

### Future Enhancements

1. **Google Cloud Vision API**: For dedicated OCR with more features
2. **Tesseract Integration**: Open-source OCR for offline processing
3. **Progress Indicators**: Show OCR progress in the UI
4. **Caching**: Cache OCR results to avoid reprocessing