# Image-to-HTML Conversion Utility

A CLI script that takes any flyer, document, layout, or design image and generates a modern, responsive, and beautifully styled single-file HTML/CSS webpage using the Google Gemini API.

## Usage

### Prerequisites
Make sure your `GEMINI_API_KEY` is set in your environment:
```powershell
$env:GEMINI_API_KEY="your-api-key"
```

### CLI Reference

Run the utility using:
```bash
image-to-html -f <path-to-image> [-o <path-to-output-html>] [-m <gemini-model>]
```

### Example
```bash
image-to-html -f "E:\DeenOps\Muhaimin Welfare Trust\04_Social_Welfare\Rashan\donation_drive\base.jpeg"
```
This will generate `base.html` in the same directory.
