# Sentence-Level Sentiment Analysis of Shakespeare's Plays Using the ChatGPT API

This repository contains a sentence-level sentiment and emotion analysis project based on Shakespeare's plays.

The project extracts spoken lines from Shakespeare XML files, selects major characters, applies Flair sentiment classification, and uses the OpenAI API to assign an emotion and sentiment label to each sentence. The resulting annotations are stored in JSON and Excel files and are subsequently used for statistical analysis and visualization.

## Project Overview

The analysis consists of two main stages.

### Part 1: Data Preparation and Flair Sentiment Analysis

1. Parse a Shakespeare play from an XML file.
2. Extract the spoken lines together with their act, scene, speaker, and sentence number.
3. Identify speakers who:

   * appear in every act of the play; and
   * have at least 50 extracted sentences.
4. Select two eligible speakers.
5. Apply Flair's pretrained sentiment classifier to each selected sentence.

Flair assigns:

* `POSITIVE` or `NEGATIVE`
* a confidence score between 0 and 1

### Part 2: GPT Emotion and Sentiment Analysis

The selected sentences are sent individually to the OpenAI API.

For each sentence, `gpt-4o-mini` predicts:

* one main emotion:

  * anger
  * anticipation
  * disgust
  * fear
  * joy
  * sadness
  * surprise
  * trust
* one sentiment:

  * positive
  * negative
  * neutral

The GPT API is configured to return a JSON object for each sentence. The current implementation uses a temperature of `0.7`.

For the Hamlet experiment included in this repository, the analysis focuses on:

* Hamlet
* King Claudius

The script also draws a random sample of 100 sentences from the combined sentences of these two characters.

## Dataset

The `dataset/` directory contains eight plays from the NLTK Shakespeare XML corpus:

* `a_and_c.xml` — *Antony and Cleopatra*
* `dream.xml` — *A Midsummer Night's Dream*
* `hamlet.xml` — *Hamlet*
* `j_caesar.xml` — *Julius Caesar*
* `macbeth.xml` — *Macbeth*
* `merchant.xml` — *The Merchant of Venice*
* `othello.xml` — *Othello*
* `r_and_j.xml` — *Romeo and Juliet*

The extraction script treats each spoken line in the XML data as a sentence-level analysis unit.

## Repository Structure

```text
.
├── dataset/
│   ├── a_and_c.xml
│   ├── dream.xml
│   ├── hamlet.xml
│   ├── j_caesar.xml
│   ├── macbeth.xml
│   ├── merchant.xml
│   ├── othello.xml
│   └── r_and_j.xml
│
├── instruction/
│   └── Exercise 06.pdf
│
├── report/
│   └── discussion.txt
│
├── results/
│   ├── all_sentences_a_and_c.json
│   ├── all_sentences_dream.json
│   ├── all_sentences_hamlet.json
│   ├── all_sentences_j_caesar.json
│   ├── all_sentences_macbeth.json
│   ├── all_sentences_merchant.json
│   ├── all_sentences_othello.json
│   ├── all_sentences_r_and_j.json
│   ├── selected_speakers_hamlet.json
│   └── sentiment_analysis_hamlet.xlsx
│
├── scripts/
│   ├── part1_flair_sentiment_skeleton.py
│   ├── part1_sentence_extractor_skeleton.py
│   ├── part1_speaker_selector_skeleton.py
│   ├── part2_call_API.py
│   ├── part2_plots.py
│   ├── part2_sentiment_stats.py
│   ├── sample_part1_flair_sentiment.py
│   ├── sample_part1_sentence_extractor.py
│   └── sample_part1_speaker_selector.py
│
└── visualizations/
    ├── play_claudius_sentiment_development.png
    ├── play_hamlet_sentiment_development.png
    ├── plot_1.png
    ├── plot_2.png
    └── plot_3.png
```

The files ending in `_skeleton.py` are incomplete exercise templates. The corresponding `sample_part1_*.py` files contain implemented examples for the first part of the workflow.

## Requirements

The repository does not currently include a `requirements.txt` file. Based on the imports used by the scripts, the project requires:

* Python 3.9 or later
* `openai`
* `flair`
* `openpyxl`
* `pandas`
* `matplotlib`
* `tqdm`

Install the required packages with:

```bash
pip install openai flair openpyxl pandas matplotlib tqdm
```

## OpenAI API Configuration

An OpenAI API key is required to run `part2_call_API.py`.

Set the `OPENAI_API_KEY` environment variable before running the script.

On macOS or Linux:

```bash
export OPENAI_API_KEY="your-api-key"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

Do not place an API key directly in the source code or commit it to the repository.

## Usage

Run the commands from the repository root unless the file paths inside a script have been adjusted.

### 1. Extract Sentences

The implemented extraction example is:

```bash
python scripts/sample_part1_sentence_extractor.py
```

This script parses a Shakespeare XML file and produces a JSON file containing sentence-level records.

Each extracted record includes information such as:

```json
{
  "act": "ACT I",
  "scene": "SCENE I",
  "speaker": "HAMLET",
  "sentence number": 1,
  "text": "Example sentence"
}
```

Before running the script, check that the selected play and its XML path correspond to the location of the files on your system.

### 2. Select Speakers

Run:

```bash
python scripts/sample_part1_speaker_selector.py
```

The script calculates the number of sentences and represented acts for each speaker. It then asks the user to select two speakers who appear in every act and have at least 50 sentences.

The selected sentences are saved in a file following this naming pattern:

```text
selected_speakers_<play_name>.json
```

### 3. Apply Flair Sentiment Analysis

Run:

```bash
python scripts/sample_part1_flair_sentiment.py
```

The script applies Flair's pretrained sentiment model to every selected sentence and adds a field in the following format:

```json
{
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.98
  }
}
```

### 4. Run GPT Emotion and Sentiment Analysis

The API script uses command-line arguments:

```bash
python scripts/part2_call_API.py \
  <input_json_file> \
  <output_excel_file> \
  <max_sentences_per_speaker>
```

Example:

```bash
python scripts/part2_call_API.py \
  results/selected_speakers_hamlet.json \
  results/sentiment_analysis_hamlet.xlsx \
  50
```

The script reads the Flair-annotated JSON data, sends each sentence to `gpt-4o-mini`, and stores the combined Flair and GPT annotations in an Excel workbook.

The output contains the following columns:

* `act`
* `scene`
* `speaker`
* `sentence number`
* `text`
* `flair_label`
* `flair_score`
* `gpt_main_emotion`
* `gpt_sentiment`

### 5. Calculate Statistics

Run:

```bash
python scripts/part2_sentiment_stats.py
```

This script reads the Excel results and calculates sentiment and emotion statistics for the analyzed characters.

Before running it, update the `INPUT_PATH` variable. The current script contains an absolute local file path that will not work on another computer without modification:

```python
INPUT_PATH = "path/to/sentiment_analysis_hamlet.xlsx"
```

### 6. Generate Visualizations

Run:

```bash
python scripts/part2_plots.py
```

The script generates visualizations comparing Flair and GPT sentiment results and examining sentiment development across the play.

The repository currently includes visualizations for Hamlet and King Claudius in the `visualizations/` directory.

## Output

The main experiment output is:

```text
results/sentiment_analysis_hamlet.xlsx
```

It combines:

* sentence metadata from the Shakespeare XML file;
* binary sentiment predictions from Flair;
* Flair confidence scores;
* eight-category emotion predictions from GPT;
* three-category sentiment predictions from GPT.

The `results/` directory also contains the intermediate sentence extraction files and the selected-speaker data for Hamlet.

## Methodological Notes

The two systems do not use identical label sets:

| System | Output                                   |
| ------ | ---------------------------------------- |
| Flair  | Positive or negative sentiment           |
| GPT    | Positive, negative, or neutral sentiment |
| GPT    | One of eight main emotions               |

Because Flair does not provide a neutral category in this workflow, direct comparisons between Flair and GPT should take this difference into account.

The analysis is performed sentence by sentence. Consequently, predictions are based on isolated spoken lines rather than the wider dramatic context of the scene or play. This can be challenging for Shakespearean language because individual sentences may contain ambiguity, irony, figurative language, or context-dependent emotion.

## Current Limitations

* The repository does not include a `requirements.txt` file.
* Some scripts contain local or hard-coded paths that must be changed before use.
* The Part 1 skeleton files contain unimplemented `pass` statements and are not directly runnable.
* The GPT analysis in `part2_call_API.py` is specifically configured for Hamlet and King Claudius.
* The `max_sentences_per_speaker` command-line argument is parsed, but the current processing function uses the complete sentence lists for Hamlet and King Claudius rather than applying that value as a limit.
* Random sampling is not assigned a fixed random seed, so the sampled 100 sentences may differ between runs.
* Sentence-level analysis does not include the broader context of surrounding dialogue.
* No automated tests are currently included.
* No license file is currently provided.

## Possible Improvements

Future development could include:

* adding a `requirements.txt` file;
* replacing hard-coded paths with command-line arguments;
* making the play and speaker names configurable;
* applying the requested sentence limit consistently;
* setting a random seed for reproducible sampling;
* adding error handling and API retry logic;
* including scene-level or dialogue-level context;
* evaluating agreement between Flair, GPT, and manual annotations;
* adding automated tests;
* adding an explicit software and dataset license.

## Acknowledgements

The Shakespeare XML files used in this project come from the NLTK Shakespeare corpus.

The project uses:

* Flair for pretrained binary sentiment classification;
* the OpenAI API for sentence-level emotion and sentiment analysis;
* pandas and openpyxl for result processing;
* matplotlib for visualization.
