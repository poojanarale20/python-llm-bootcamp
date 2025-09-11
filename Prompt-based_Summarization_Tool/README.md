# Prompt-Based Summarization Tool (Offline - Transformers)

A command-line tool for summarizing news articles or any text files using open-source models (e.g., facebook/bart-large-cnn) from the Hugging Face Transformers library. Works completely offline after the initial model download.

## Features
- Summarize news articles and long texts using HuggingFace models.
- Customize summary with `max_length`, `min_length`, and sampling.
- Save the summary to a `.txt` file.
- CLI-based — simple and fast.
- No API key or internet access required after downloading the model.
- No billing or quota issues.

## Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. **Summarize a text file:**
   ```bash
   python summarizer.py sample_article.txt
   ```

2. **Customize summary:**
   ```bash
   python summarizer.py sample_article.txt --max_length 100 --min_length 20 --sample
   ```

3. **Choose a different model:**
   ```bash
   python summarizer.py sample_article.txt --model facebook/bart-large-cnn
   ```

4. **Save summary to a file:**
   ```bash
   python summarizer.py sample_article.txt --output summary.txt
   ```

## Example
- Input: `sample_article.txt`
- Output: `summary.txt`

## Notes
- The first run will download the model if not already present (requires internet). Subsequent runs are fully offline.
- For best results, use articles or texts up to a few thousand characters.
