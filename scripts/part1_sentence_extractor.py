"""
Part 0a: Sentence Extraction from a Shakespeare XML file.

- Parses one XML play file (from the NLTK Shakespeare XML corpus).
- Extracts all spoken lines as "sentences".
- Stores them in all_sentences.json.

"""

import json
import xml.etree.ElementTree as ET


def parse_xml(path: str) -> ET.Element:
    """
    Parse the XML file and return the root element.

    Args:
        path (str): Path to the XML file.

    Returns:
        xml.etree.ElementTree.Element: Root element of the parsed XML.
    """
    tree = ET.parse(path)
    return tree.getroot()


def extract_sentences(root: ET.Element) -> list[dict]:
    """
    Walk through the XML structure and extract all spoken lines.

    Args:
        root (xml.etree.ElementTree.Element): Root element of the XML.

    Returns:
        list of dict: List of sentences with metadata. More specifically:
            - act (int): Act number.
            - scene (int): Scene number.
            - speaker (str): Speaker name.
            - sentence_id (int): Unique sentence identifier.
            - text (str): The spoken line text.
    """
    sentences = []
    sentence_id = 0

    # Acts are top-level children of PLAY
    for act_number, act in enumerate(root.findall("ACT"), start=1):

        # Scenes are children of ACT
        for scene_number, scene in enumerate(act.findall("SCENE"), start=1):

            # SPEECH elements contain SPEAKER and LINE children
            for speech in scene.findall("SPEECH"):
                speaker = speech.findtext("SPEAKER", default="UNKNOWN")

                # Extract each LINE within this SPEECH
                for line in speech.findall("LINE"):
                    sentence_text = (line.text or "").strip()

                    # Skip empty lines
                    if not sentence_text:
                        continue

                    sentence_id += 1

                    sentences.append(
                        {
                            "act": act_number,
                            "scene": scene_number,
                            "speaker": speaker,
                            "sentence_id": sentence_id,
                            "text": sentence_text,
                        }
                    )

    return sentences


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


def main(play_name):
    print(f"Extracting sentences from {play_name} Shakespeare play...")

    input_path = f"{play_name}.xml"
    output_path = f"all_sentences_{play_name}.json"

    print(f"Processing: {play_name}")
    print(f"  Reading from: {input_path}")

    # Parse XML and extract sentences
    root = parse_xml(input_path)
    sentences = extract_sentences(root)

    # Save to JSON
    save_json(sentences, output_path)

    print(f"  Extracted {len(sentences)} sentences")
    print(f"  Saved to: {output_path}")

    print("Extraction complete!")


if __name__ == "__main__":
    play_name = "dream"  # Placeholder for selected play
    main(play_name)
