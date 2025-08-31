# PDF to PNG Converter

A Python script to batch-convert PDF files into high-quality images inside WSL.  
Perfect for scanned documents, reports, or extracting images from multipage PDFs.

## ✨ Features

- Batch conversion of all PDFs in `./pdfs`
- Save output images in `./images`
- Adjustable DPI for sharpness (default 300)
- Optional auto-trim of black borders
- Supports PNG (lossless) and JPEG (smaller size)

## 🚀 Usage

```bash
pip install pdf2image pillow
sudo apt-get install poppler-utils  # required for pdf2image in WSL
python convert_pdfs.py
```
