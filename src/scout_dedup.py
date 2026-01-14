import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

def load_all_signals(directory):
    all_signals = []
    files = [f for f in os.listdir(directory) if f.endswith(".json")]
    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    all_signals.extend(data)
                else:
                    all_signals.append(data)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {filepath}")
    return all_signals, files

def get_authority_score(url):
    AUTHORITY_RANK = {
        'reuters.com': 10,
        'bloomberg.com': 10,
        'wsj.com': 10,
        'spacenews.com': 9,
        'eetimes.com': 9,
        'semiengineering.com': 9,
        'world-nuclear-news.org': 9,
        'techcrunch.com': 7,
        'electrek.co': 7,
        'arstechnica.com': 7,
        'default': 5
    }
    for domain, score in AUTHORITY_RANK.items():
        if domain in url:
            return score
    return AUTHORITY_RANK['default']

def semantic_dedup(signals, threshold=0.85):
    if not signals:
        return []

    print(f"Starting semantic deduplication for {len(signals)} signals...")
    
    # Use a small, efficient model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Prepare texts for embedding
    texts = []
    for s in signals:
        title = s.get('title', '') or s.get('body', '') or ''
        summary = s.get('summary', '') or s.get('snippet', '') or ''
        texts.append(f"{title} {summary}")

    print("Encoding signals...")
    embeddings = model.encode(texts)
    
    print("Calculating similarity matrix...")
    sim_matrix = cosine_similarity(embeddings)
    
    to_remove = set()
    for i in range(len(signals)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(signals)):
            if j in to_remove:
                continue
            
            if sim_matrix[i][j] > threshold:
                # Deduplicate: Keep more authoritative or more detailed one
                score_i = get_authority_score(signals[i].get('link', signals[i].get('url', '')))
                score_j = get_authority_score(signals[j].get('link', signals[j].get('url', '')))
                
                if score_i >= score_j:
                    to_remove.add(j)
                else:
                    to_remove.add(i)
                    break # i is removed, stop checking for it

    deduped = [s for idx, s in enumerate(signals) if idx not in to_remove]
    print(f"Deduplication complete. Reduced from {len(signals)} to {len(deduped)} signals.")
    return deduped

def main():
    incoming_dir = "data/Incoming"
    if not os.path.exists(incoming_dir):
        print("Incoming directory not found.")
        return

    signals, original_files = load_all_signals(incoming_dir)
    if not signals:
        print("No signals to deduplicate.")
        return

    deduped_signals = semantic_dedup(signals)
    
    # Overwrite the original files with a single consolidated and deduped file
    # First, delete old files to avoid confusion
    for f in original_files:
        os.remove(os.path.join(incoming_dir, f))
    
    # Save deduped signals
    output_file = os.path.join(incoming_dir, f"consolidated_signals_{int(time.time())}.json")
    with open(output_file, 'w') as f:
        json.dump(deduped_signals, f, indent=2)
    print(f"Consolidated and deduplicated signals saved to {output_file}")

if __name__ == "__main__":
    main()
