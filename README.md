# NLP-ASD  
Study repo focused on **non-literal language (sarcasm)** and **autism spectrum disorder (ASD)**—building a pipeline to collect, filter, and analyze sarcasm-related discussions from public web sources.

## Project overview
This repository supports a study on how people on the autism spectrum **describe, interpret, and react to sarcasm** in online discussions.

Core goal:
- **Scrape public text → run a sarcasm detector → keep sarcasm-relevant content → analyze ASD-related reactions**.

---

## Research goal
**High-level question**
> How do people on the autism spectrum describe their reactions to sarcasm, and what patterns appear in their responses (e.g., confusion, distress, coping strategies, learning, cues used, context dependence)?

This repo focuses on:
1. Collecting relevant text from public web sources (web scraping)
2. **Filtering scraped text using a trained sarcasm detection model**
3. Preparing a dataset for analysis (manual coding, NLP features, clustering, sentiment/emotion, etc.)

---

## Pipeline

### 1) Web scraping (collection)
A Playwright-based scraper discovers and opens search results, then extracts paragraph-level content.

- Script: `scrap_updated.py`
- Output (recommended): raw extracted paragraphs + metadata (URL, timestamp, position, etc.)

### 2) Model-based sarcasm filtering (main use)
The final sarcasm detection model (trained/selected in this repo) will be used to filter the scraped data.

Filtering concept:
- Run the model on each scraped text segment (paragraph/post)
- Keep items with sarcasm probability above a threshold (e.g., `p >= 0.5`, tune as needed)
- Save:
  - `text`
  - `sarcasm_score`
  - `is_sarcastic` (thresholded label)
  - metadata (source URL, timestamp)

This replaces the current keyword-only heuristic (e.g., checking for the word `"sarcasm"`).

---

## Sarcasm Detection Baselines (LLM + RoBERTa)

This repo includes two notebooks to build/benchmark sarcasm detection approaches:

1. **LLM prompt benchmark**: prompt-based sarcasm classification across datasets  
2. **RoBERTa-Large baseline (TPU-safe)**: supervised training + evaluation in Colab/TPU

### Notebooks
- **`SarcasmGPTBenchmark.ipynb`**
  - Prompt-based sarcasm benchmark across datasets
  - Configurable prompt versions and metrics reporting

- **`sarcasm_roberta_large_full_tpu.ipynb`**
  - TPU-safe training pipeline for **RoBERTa-Large**
  - Produces evaluation metrics (e.g., accuracy/F1) and model outputs

---

## Datasets used (in the notebooks)

### Hugging Face
- `cardiffnlp/tweet_eval` (`irony`)
- `tasksource/figlang2020-sarcasm`

### Kaggle (via `kagglehub`)
- `danofer/sarcasm` (SARC-style Reddit sarcasm)

> Additional datasets may be referenced in notebooks. Please comply with each dataset’s license/terms.

---

## Ethics & responsible research (important)
- Respect website/platform Terms of Service and robots policies.
- Prefer public content and minimize collection of personal identifiers.
- Avoid re-publishing raw scraped text unless permitted
