import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
from src.config import PATHS, STRATEGY

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

def get_authority_score(signal):
    url = signal.get('link', signal.get('url', ''))
    # Preference for newer signals when semantics are near-identical
    # date can be a timestamp or a string, let's try to normalize or check existence
    timestamp = signal.get('date', 0)
    if timestamp is None:
        timestamp = 0
    if isinstance(timestamp, str): # Handle string dates if necessary
        timestamp = 0 # Simple fallback
    
    AUTHORITY_RANK = {
        'reuters.com': 100,
        'bloomberg.com': 100,
        'wsj.com': 100,
        'spacenews.com': 90,
        'eetimes.com': 90,
        'world-nuclear-news.org': 90,
        'techcrunch.com': 70,
        'default': 50
    }
    
    base_score = AUTHORITY_RANK['default']
    for domain, score in AUTHORITY_RANK.items():
        if domain in url:
            base_score = score
            break
            
    # Time-weighting: add bias for newer signals
    # We use a relative time score; this assumes signals are from a similar timeframe
    return base_score + (timestamp / 1000000) # Subtle boost for newer timestamps

def semantic_dedup(signals, threshold=None):
    if threshold is None:
        threshold = STRATEGY["RELEVANCE_THRESHOLD"]
    
    if not signals:
        return []

    print(f"Starting semantic deduplication for {len(signals)} signals...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    texts = []
    for s in signals:
        title = s.get('title', '') or s.get('body', '') or ''
        summary = s.get('summary', '') or s.get('snippet', '') or s.get('content', '') or ''
        texts.append(f"{title} {summary}")

    embeddings = model.encode(texts)
    sim_matrix = cosine_similarity(embeddings)
    
    to_remove = set()
    for i in range(len(signals)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(signals)):
            if j in to_remove:
                continue
            
            if sim_matrix[i][j] > threshold:
                score_i = get_authority_score(signals[i])
                score_j = get_authority_score(signals[j])
                
                if score_i >= score_j:
                    to_remove.add(j)
                else:
                    to_remove.add(i)
                    break 

    deduped = [s for idx, s in enumerate(signals) if idx not in to_remove]
    print(f"Deduplication complete. Reduced from {len(signals)} to {len(deduped)} signals.")
    return deduped

def main():
    incoming_dir = PATHS["INCOMING"]
    if not os.path.exists(incoming_dir):
        return

    signals, original_files = load_all_signals(incoming_dir)
    if not signals:
        return

    deduped_signals = semantic_dedup(signals)
    
    # Clean workspace
    for f in original_files:
        os.remove(os.path.join(incoming_dir, f))
    
    # Save consolidated
    output_file = os.path.join(incoming_dir, f"consolidated_signals_{int(time.time())}.json")
    with open(output_file, 'w') as f:
        json.dump(deduped_signals, f, indent=2)
    print(f"Consolidated and deduplicated signals saved to {output_file}")

if __name__ == "__main__":
    main()
