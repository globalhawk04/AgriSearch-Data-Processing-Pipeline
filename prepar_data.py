# /home/j/Desktop/aggs/tutorial/agri/data/prepare_data.py
# --- UPDATED to use 51-100 word snippet AS 'summary' ---

import json
import os
import sys
# Requires: pip install langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Configuration ---
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
KEYWORD_SNIPPET_START_WORD = 0 # For the snippet function
KEYWORD_SNIPPET_LENGTH = 500 # For the snippet function

INPUT_FILENAME = 'wiscon_kstate_osu_atm_missu_merge.json' # Input contains all fields
OUTPUT_FILENAME = 'wiscon_kstate_osu_atm_missu_merge_chunked.json' # Output includes snippet as 'summary'
# ---------------------

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

# Helper function for Keyword/Author snippet (No changes needed)
def generate_keyword_snippet_51_100(text):
    if not text or not isinstance(text, str): return ""
    words = text.split(); snippet = ""
    if len(words) > KEYWORD_SNIPPET_START_WORD:
        start = KEYWORD_SNIPPET_START_WORD; end = start + KEYWORD_SNIPPET_LENGTH
        snippet_words = words[start:end]; snippet = ' '.join(snippet_words)
        prefix = "... "; suffix = " ..." if len(words) > end else ""
        snippet = prefix + snippet + suffix
    else: snippet = "[Text too short for 51-100 word snippet]"
    return snippet

def process_json_file(input_path, output_path):
    all_chunks = []
    doc_counter = 0

    print(f"Starting processing of '{os.path.basename(input_path)}'...")
    print(f"Using Chunk Size: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=False,
    )

    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'", file=sys.stderr); return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_path}'.", file=sys.stderr); return
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr); return

    if not isinstance(data, list):
        print(f"Error: Expected input JSON to be a list.", file=sys.stderr); return

    print(f"Loaded {len(data)} documents from input file.")

    for item in data:
        doc_counter += 1
        pdf_url = item.get('pdf_url')
        pdf_text = item.get('txt ')
        headline_from_item = item.get('headline') # Renamed to avoid confusion with new 'headline' field in chunk
        jpg_url = item.get('jpg_url')
        pub_date = item.get('pub_date')
        school_name = item.get('school') # This is the variable holding the 'school' value
        sort_date = item.get('sort_date')
        main_url = item.get('main_url')

        if not pdf_url:
            pdf_url = f"unknown_doc_{doc_counter}"
            print(f"Warning: Document {doc_counter} missing 'pdf_url'. Using placeholder '{pdf_url}'.", file=sys.stderr)
        if not pdf_text or not isinstance(pdf_text, str) or not pdf_text.strip():
            print(f"Warning: Document {doc_counter} ('{pdf_url}') has missing or invalid 'pdf_text'. Skipping.", file=sys.stderr)
            continue

        # --- Generate the snippet for the 'summary' field ---
        snippet_text_for_chunk = generate_keyword_snippet_51_100(pdf_text) # Renamed variable for clarity
        # -----------------------------------------------------

        # Optional checks for missing jpg_url, pub_date
        if not jpg_url: print(f"Warning: Document {doc_counter} ('{pdf_url}') missing 'jpg_url'.", file=sys.stderr)
        if not pub_date: print(f"Warning: Document {doc_counter} ('{pdf_url}') missing 'pub_date'.", file=sys.stderr)

        try:
            text_chunks = text_splitter.split_text(pdf_text)

            if not text_chunks:
                print(f"Warning: Document {doc_counter} ('{pdf_url}') resulted in zero chunks.", file=sys.stderr)
                continue

            for i, chunk_text in enumerate(text_chunks):
                chunk_id = f"{doc_counter}_chunk{i}"
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "pdf_url": pdf_url,
                    "chunk_text": chunk_text, # This is the main text content for the chunk
                    "headline": headline_from_item, # Using the variable for headline
                    "jpg_url": jpg_url,
                    "pub_date": pub_date,
                    'main_url':main_url,
                    'school':school_name, # <--- FIXED HERE: Key is 'school', value is from 'school_name' variable
                    'sort_date': sort_date,
                    'snippet': snippet_text_for_chunk # <--- FIXED HERE: Added the 'snippet' field!
                })
        except Exception as e:
            print(f"Error chunking document {doc_counter} ('{pdf_url}'): {e}", file=sys.stderr)
            continue

    print(f"Generated {len(all_chunks)} chunks from {doc_counter} documents processed.")

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(all_chunks, outfile, indent=2, ensure_ascii=False)
        print(f"Successfully saved chunked data (with snippet as summary) to '{os.path.basename(output_path)}'")
    except Exception as e:
        print(f"Error writing output file '{output_path}': {e}", file=sys.stderr)

if __name__ == "__main__":
    script_dir = get_script_directory()
    input_file = os.path.join(script_dir, INPUT_FILENAME)
    output_file = os.path.join(script_dir, OUTPUT_FILENAME)
    process_json_file(input_file, output_file)