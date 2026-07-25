"""
Part 0b: Speaker Selection.

- Reads all_sentences.json.
- Computes statistics for each speaker.
- Checks which speakers appear in every act and have at least MIN_SENTENCES.
- Lets the user choose two speakers (must satisfy the conditions).
- Writes sentences of the selected speakers to selected_speakers.json.
"""

import json

MIN_SENTENCES = 50  # required minimum number of sentences per speaker


def load_sentences(path) -> list[dict]:
    """
    Load the JSON file with all sentences.

    Args:
        path (str): Path to the JSON file.

    Returns:
        list: List of sentence dictionaries.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_statistics(
        sentences: list[dict]) -> tuple[set, dict[str, int], dict[str, set]]:
    """
    Compute the set of acts and for each speaker
    the sentence count and acts spoken in.

    Args:
        sentences (list): List of sentence dictionaries.

    Returns:
        tuple: (acts_in_play, speaker_counts, speaker_acts)
    """
    acts_in_play = set()
    speaker_counts = {}   # speaker -> int
    speaker_acts = {}     # speaker -> set of acts

    for s in sentences:
        act = s["act"]
        speaker = s["speaker"]

        acts_in_play.add(act)

        if speaker not in speaker_counts:
            speaker_counts[speaker] = 0
        speaker_counts[speaker] += 1

        if speaker not in speaker_acts:
            speaker_acts[speaker] = set()
        speaker_acts[speaker].add(act)

    return acts_in_play, speaker_counts, speaker_acts


def find_valid_speakers(
        acts_in_play: set,
        speaker_counts: dict,
        speaker_acts: dict,
        min_sentences: int) -> list[str]:
    """
    Return a list of speakers that meet both conditions.

    Args:
        acts_in_play (set): Set of all acts in the play.
        speaker_counts (dict): Mapping of speaker to their sentence count.
        speaker_acts (dict): Mapping of speaker to the set of acts they spoke in.
        min_sentences (int): Minimum number of sentences required.

    Returns:
        list: List of valid speakers.
    """
    valid = []
    for speaker, count in speaker_counts.items():
        if count >= min_sentences and speaker_acts[speaker] == acts_in_play:
            valid.append(speaker)
    return valid


def print_statistics(acts_in_play, speaker_counts, speaker_acts):
    """
    Print a small table of speakers and their stats.

    Args:
        acts_in_play (set): Set of all acts in the play.
        speaker_counts (dict): Mapping of speaker to their sentence count.
        speaker_acts (dict): Mapping of speaker to the set of acts they spoke in.

    Returns:
        None
    """
    print("Acts in play:", sorted(acts_in_play))
    print("\nSpeaker statistics:")
    print("{:<25} {:>10} {:>20}".format("Speaker", "Sentences", "Acts spoken in"))
    print("-" * 60)

    # build list sorted by count
    sortable = []
    for speaker, count in speaker_counts.items():
        sortable.append((count, speaker))  # count first

    sortable.sort(reverse=True)  # sorts by count, then speaker

    for count, speaker in sortable:
        acts = sorted(speaker_acts[speaker])
        print("{:<25} {:>10} {:>20}".format(speaker, count, str(acts)))


def ask_for_speakers(valid_speakers: list[str]) -> list[str]:
    """
    Ask the user to type two speakers.
    Speakers must be in the list of valid_speakers.

    Args:
        valid_speakers (list): List of valid speaker names.

    Returns:
        list: List of chosen speaker names.
    """
    print("Speakers that meet the conditions")
    print(f"(in every act and at least {MIN_SENTENCES} sentences):")
    for sp in valid_speakers:
        print("  -", sp)
    print()

    chosen = []
    while len(chosen) < 2:
        name = input(f"Enter name of speaker {len(chosen) + 1}: ").strip()
        if name not in valid_speakers:
            print("This speaker does not meet the conditions "
                  "or is unknown. Try again.")
        elif name in chosen:
            print("You already chose this speaker. Pick a different one.")
        else:
            chosen.append(name)

    return chosen


def filter_sentences(
        sentences: list[dict], chosen_speakers: list[str]) -> list[dict]:
    """
    Return only sentences spoken by the chosen speakers.

    Args:
        sentences (list): List of sentence dictionaries.
        chosen_speakers (list): List of chosen speaker names.

    Returns:
        list: Filtered list of sentence dictionaries.
    """
    return [s for s in sentences if s["speaker"] in chosen_speakers]


def save_json(data, path):
    """
    Save Python data as JSON to the given path.

    Args:
        data: Python data to save.
        path (str): Path to the output JSON file.

    Returns:
        None
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(play_name):
    sentences = load_sentences(f"all_sentences_{play_name}.json")
    acts_in_play, speaker_counts, speaker_acts = compute_statistics(sentences)

    print_statistics(acts_in_play, speaker_counts, speaker_acts)

    valid_speakers = find_valid_speakers(
        acts_in_play, speaker_counts, speaker_acts, MIN_SENTENCES
    )

    if len(valid_speakers) < 2:
        print("Error: fewer than two speakers meet the conditions.")
        print("Try using a different play.")
        exit(1)

    chosen = ask_for_speakers(valid_speakers)
    selected_sentences = filter_sentences(sentences, chosen)
    save_json(selected_sentences, f"selected_speakers_{play_name}.json")

    print(
        f"Saved {len(selected_sentences)} sentences for "
        f"{play_name} to selected_speakers_{play_name}.json")


if __name__ == "__main__":
    play_name = "dream"  # Placeholder for selected play
    main(play_name)
