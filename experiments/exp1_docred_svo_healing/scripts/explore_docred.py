#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DocRED Dataset Explorer

This script explores and provides statistics about the DocRED dataset.

Original DocRED Dataset:
- Repository: https://github.com/thunlp/DocRED
- Paper: "DocRED: A Large-Scale Document-Level Relation Extraction Dataset"
- Authors: Yuan Yao, Deming Ye, Peng Li, Xu Han, Yankai Lin, Zhenghao Liu, Zhiyuan Liu, Lixin Huang, Jie Zhou, Maosong Sun
- Publication: ACL 2019

This script is used in the self-healing knowledge graph project to analyze and 
understand the dataset characteristics.
"""

import os
import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_json(file_path):
    """Load a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_dataset_paths():
    """Get paths to dataset files."""
    # Navigate to the data directory (assuming script is in scripts/ directory)
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent / "data"
    
    dataset_files = {
        "train": data_dir / "train_annotated.json",
        "dev": data_dir / "dev.json",
        "test": data_dir / "test.json"
    }
    
    # Check if files exist
    for split, path in dataset_files.items():
        if not path.exists():
            print(f"Warning: {split} file not found at {path}")
    
    return dataset_files

def analyze_dataset(data):
    """Analyze dataset and return statistics."""
    if not data:
        return None
    
    # Basic counts
    num_docs = len(data)
    total_entities = sum(len(doc.get("entities", [])) for doc in data)
    total_relations = sum(len(doc.get("relations", [])) for doc in data if "relations" in doc)
    
    # Count sentences and tokens
    total_sents = sum(len(doc.get("sents", [])) for doc in data)
    total_tokens = sum(sum(len(sent) for sent in doc.get("sents", [])) for doc in data)
    
    # Entity type distribution
    entity_types = Counter()
    for doc in data:
        for entity in doc.get("entities", []):
            entity_types[entity.get("type", "unknown")] += 1
    
    # Relation type distribution
    relation_types = Counter()
    for doc in data:
        for relation in doc.get("relations", []):
            relation_types[relation.get("r", "unknown")] += 1
    
    return {
        "num_docs": num_docs,
        "total_entities": total_entities,
        "total_relations": total_relations,
        "total_sents": total_sents,
        "total_tokens": total_tokens,
        "entity_types": entity_types,
        "relation_types": relation_types,
        "avg_entities_per_doc": total_entities / num_docs if num_docs else 0,
        "avg_relations_per_doc": total_relations / num_docs if num_docs else 0,
        "avg_sents_per_doc": total_sents / num_docs if num_docs else 0,
        "avg_tokens_per_doc": total_tokens / num_docs if num_docs else 0
    }

def plot_distribution(counter, title, filename=None):
    """Plot distribution of a counter."""
    labels, values = zip(*counter.most_common(10))  # Get top 10
    
    # Create horizontal bar chart
    plt.figure(figsize=(10, 6))
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, values)
    plt.yticks(y_pos, labels)
    plt.xlabel('Count')
    plt.title(title)
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()

def print_statistics(stats, split_name):
    """Print dataset statistics."""
    print(f"\n==== {split_name.upper()} DATASET STATISTICS ====")
    print(f"Number of documents: {stats['num_docs']}")
    print(f"Total entities: {stats['total_entities']} (avg: {stats['avg_entities_per_doc']:.2f} per doc)")
    print(f"Total relations: {stats['total_relations']} (avg: {stats['avg_relations_per_doc']:.2f} per doc)")
    print(f"Total sentences: {stats['total_sents']} (avg: {stats['avg_sents_per_doc']:.2f} per doc)")
    print(f"Total tokens: {stats['total_tokens']} (avg: {stats['avg_tokens_per_doc']:.2f} per doc)")
    
    print("\nTop 5 entity types:")
    for entity_type, count in stats['entity_types'].most_common(5):
        print(f"  - {entity_type}: {count}")
    
    print("\nTop 5 relation types:")
    for relation_type, count in stats['relation_types'].most_common(5):
        print(f"  - {relation_type}: {count}")

def main():
    """Main function to explore the DocRED dataset."""
    print("DocRED Dataset Explorer")
    print("=======================")
    print("Original dataset by Yuan Yao et al., ACL 2019")
    print("Repository: https://github.com/thunlp/DocRED")
    print("=======================\n")
    
    # Get dataset paths
    dataset_files = get_dataset_paths()
    
    # Process each split
    for split, path in dataset_files.items():
        if not path.exists():
            continue
            
        print(f"Loading {split} dataset from {path}...")
        data = load_json(path)
        
        if data:
            stats = analyze_dataset(data)
            print_statistics(stats, split)
            
            # Create results directory for plots
            results_dir = Path(__file__).parent.parent / "results"
            results_dir.mkdir(exist_ok=True)
            
            # Generate plots
            plot_distribution(
                stats['entity_types'], 
                f'Entity Type Distribution ({split})',
                results_dir / f"{split}_entity_types.png"
            )
            plot_distribution(
                stats['relation_types'], 
                f'Relation Type Distribution ({split})',
                results_dir / f"{split}_relation_types.png"
            )
    
    print("\nAnalysis complete. Plots saved to the 'results' directory.")

if __name__ == "__main__":
    main()

