"""
Part 1a: Sentiment Analysis using Flair.

- Reads selected_speakers.json.
- Uses Flair's pre-trained sentiment model to analyze each sentence.
- Stores the results in selected_speakers.json by adding a "sentiment"
  field to each sentence.
- The sentiment field contains:
    - label (str): "POSITIVE" or "NEGATIVE"
    - score (float): confidence score between 0 and 1
    
"""

import json
from flair.models import TextClassifier
from flair.data import Sentence

MIN_SENTENCES = 50  # required minimum number of sentiment rich sentences per speaker


def load_sentences(path: str) -> list[dict]:
    """
    Load the JSON file with selected speaker sentences.

    Args:
        path (str): Path to the JSON file.

    Returns:
        list: List of sentence dictionaries.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: list[dict], path: str) -> None:
    """
    Save Python data as JSON to the given path.

    Args:
        data (list of dict): Data to save.
        path (str): Path to save the JSON file.

    Returns:
        None
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def analyze_sentiments(sentences: list[dict]) -> list[dict]:
    """
    Analyze sentiments of the given sentences using Flair.

    Only keeps sentences with sentiment score >= 0.9 (high confidence).

    Args:
        sentences (list of dict): List of sentence dictionaries.

    Returns:
        list of dict: Filtered list with only high-confidence sentiment sentences.
    """
    # Load Flair's pre-trained sentiment classifier
    print("Loading Flair sentiment model...")
    classifier = TextClassifier.load("sentiment")

    high_confidence_sentences = []

    # Analyze each sentence
    for sentence_dict in sentences:
        text = sentence_dict["text"]

        # Create a Flair sentence object and predict sentiment
        flair_sentence = Sentence(text)
        classifier.predict(flair_sentence)

        # Get the sentiment label (POSITIVE or NEGATIVE) and confidence score
        sentiment_label = flair_sentence.labels[0]

        # Only keep sentences with high confidence (>= 0.9)
        if sentiment_label.score >= 0.9:
            sentence_dict["sentiment"] = {
                "label": sentiment_label.value,
                "score": sentiment_label.score,
            }
            high_confidence_sentences.append(sentence_dict)

    return high_confidence_sentences


def has_enough_sentences(sentences: list[dict], minimum: int) -> bool:
    """
    Check if we have enough sentences for analysis.

    Args:
        sentences (list of dict): List of sentence dictionaries.
        minimum (int): Minimum number of sentences required.

    Returns:
        bool: True if we have enough sentences, False otherwise.
    """
    return len(sentences) >= minimum


if __name__ == "__main__":
    import os

    # List of Shakespeare plays to process
    play_names = [
        "a_and_c",
        "dream",
        "hamlet",
        "j_caesar",
        "macbeth",
        "merchant",
        "othello",
    ]

    print(f"Starting sentiment analysis for {len(play_names)} plays...")
    print(f"Minimum required sentences per play: {MIN_SENTENCES}\n")

    # Process each play
    for play_name in play_names:
        print(f"Processing play: {play_name}")

        # Build input and output file paths
        input_path = f"sample_data/selected/selected_speakers_{play_name}.json"
        output_path = f"sample_data/updated/updated_selected_speakers_{play_name}.json"

        # Check if input file exists
        if not os.path.exists(input_path):
            print(f"  ⚠ File not found: {input_path}")
            print(f"  Skipping {play_name}\n")
            continue

        # Load sentences from input file
        print(f"  Reading: {input_path}")
        all_sentences = load_sentences(input_path)
        print(f"  Found {len(all_sentences)} sentences")

        # Analyze sentiments and filter high-confidence sentences
        high_confidence_sentences = analyze_sentiments(all_sentences)
        print(f"  High-confidence sentences: {len(high_confidence_sentences)}")

        # Check if we have enough sentences
        if has_enough_sentences(high_confidence_sentences, MIN_SENTENCES):
            # Save the filtered sentences
            save_json(high_confidence_sentences, output_path)
            print(f"  ✓ Saved to: {output_path}")
        else:
            print(
                f"  \u2717 Error: Only {len(high_confidence_sentences)} sentences "
                f"with score >= 0.9 (need {MIN_SENTENCES})."
            )
            print("  Try selecting different speakers or a different play.")

        print()

    print("Sentiment analysis complete!")
