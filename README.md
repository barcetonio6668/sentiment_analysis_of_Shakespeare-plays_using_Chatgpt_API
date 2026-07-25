# Sentence-Level Sentiment and Emotion Analysis of Shakespeare's Plays

This repository contains a sentence-level sentiment and emotion analysis project based on Shakespeare's plays.

The workflow extracts spoken lines from Shakespeare XML files, identifies major characters, applies Flair's pretrained sentiment classifier, and uses the OpenAI API (`gpt-4o-mini`) to predict emotion and sentiment labels for each extracted line. The annotated data are stored in JSON and Excel formats for further statistical analysis and visualization.

> **Note:** Each `<LINE>` element in the Shakespeare XML corpus is treated as one analysis unit. No additional sentence segmentation is performed.

## Project Workflow

The project consists of two stages.

### Part 1: Data Preparation and Flair Sentiment Analysis

The first stage:

* extracts spoken lines from Shakespeare XML files;
* records their metadata (act, scene, speaker, etc.);
* selects speakers appearing in every act with at least 50 extracted lines;
* predicts binary sentiment using Flair.

Flair assigns:

* **POSITIVE**
* **NEGATIVE**

together with a confidence score.

### Part 2: GPT Emotion and Sentiment Analysis

The selected lines are submitted individually to the OpenAI API (`gpt-4o-mini`).

For each line, GPT predicts:

* one of eight basic emotions:

  * anger
  * anticipation
  * disgust
  * fear
  * joy
  * sadness
  * surprise
  * trust
* one sentiment label:

  * positive
  * neutral
  * negative

The annotated results are exported to Excel for statistical analysis and visualization.

## Dataset

The repository contains eight Shakespeare plays from the NLTK Shakespeare XML corpus:

* Antony and Cleopatra
* A Midsummer Night's Dream
* Hamlet
* Julius Caesar
* Macbeth
* The Merchant of Venice
* Othello
* Romeo and Juliet

The current experiment focuses on **Hamlet** and **King Claudius**.

## Repository Structure

```text
.
├── dataset/
├── instruction/
├── report/
├── results/
├── scripts/
├── visualizations/
├── README.md
└── requirements.txt
```

The `scripts/` directory contains the complete workflow, including sentence extraction, speaker selection, Flair sentiment analysis, GPT annotation, statistical analysis, and visualization.

## Installation

Clone the repository:

```bash
git clone https://github.com/barcetonio6668/sentiment_analysis_of_Shakespeare-plays_using_Chatgpt_API.git
cd sentiment_analysis_of_Shakespeare-plays_using_Chatgpt_API
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Before running the GPT annotation script, configure your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

## Usage

Run the scripts in the following order:

```bash
python scripts/sample_part1_sentence_extractor.py
python scripts/sample_part1_speaker_selector.py
python scripts/sample_part1_flair_sentiment.py
python scripts/part2_call_API.py
python scripts/part2_sentiment_stats.py
python scripts/part2_plots.py
```

## Output

The workflow produces:

* extracted sentence-level JSON files;
* selected-speaker datasets;
* Flair sentiment annotations;
* GPT emotion and sentiment annotations;
* Excel result files;
* statistical summaries;
* visualization figures.

The main output file is:

```text
results/sentiment_analysis_hamlet.xlsx
```

## Current Limitations

* Each XML `<LINE>` element is treated as one analysis unit.
* The current GPT experiment is configured for Hamlet and King Claudius.
* Some scripts still contain hard-coded paths that should be generalized.
* The skeleton scripts are intended as exercise templates and are not complete implementations.
* No automated tests are currently included.

## Future Work

Possible future improvements include:

* supporting additional Shakespeare plays;
* configurable play and speaker selection;
* improved path handling and command-line arguments;
* reproducible sampling;
* comparison with manually annotated data;
* incorporation of dialogue or scene-level context.

## Acknowledgements

This project uses:

* the NLTK Shakespeare corpus;
* Flair for pretrained sentiment classification;
* the OpenAI API for emotion and sentiment prediction;
* pandas, openpyxl, and matplotlib for data processing and visualization.

---

**Maintainer:** liuxduan  
**Last updated:** July 2026
