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

def print_sample_document(data):
    """Print a sample document to understand its structure."""
    if data and len(data) > 0:
        sample = data[0]
        print("\nSample Document Structure:")
        for key, value in sample.items():
            if isinstance(value, list) and len(value) > 0:
                print(f"- {key}: {type(value)} with {len(value)} items")
                if key == "entities" and len(value) > 0:
                    print(f"  Sample entity: {value[0]}")
                elif key == "relations" and len(value) > 0:
                    print(f"  Sample relation: {value[0]}")
                elif key == "sents" and len(value) > 0:
                    print(f"  Sample sentence: {value[0][:5]}...")
            else:
                print(f"- {key}: {type(value)}")

def get_dataset_paths():
    """Get paths to dataset files."""
    # Navigate to the data directory (assuming script is in scripts/ directory)
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent / "data"
    raw_data_dir = data_dir / "raw_data"
    
    dataset_files = {
        "train": raw_data_dir / "train_annotated.json",
        "dev": raw_data_dir / "dev.json",
        "test": raw_data_dir / "test.json"
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
    
    # Print sample document to understand structure
    print_sample_document(data)
    
    # Extract entities and relations
    total_entities = 0
    total_relations = 0
    entity_types = Counter()
    relation_types = Counter()
    
    # Count sentences and tokens
    total_sents = 0
    total_tokens = 0
    
    # Analyze each document
    for doc in data:
        # Process entities
        doc_entities = doc.get("vertexSet", []) if "vertexSet" in doc else doc.get("entities", [])
        total_entities += len(doc_entities)
        
        # Extract entity types
        for entity in doc_entities:
            # Handle different entity formats
            if isinstance(entity, dict) and "type" in entity:
                entity_types[entity["type"]] += 1
            elif isinstance(entity, list) and len(entity) > 0:
                # In DocRED, vertexSet is a list of mentions of the same entity
                if "type" in entity[0]:
                    entity_types[entity[0]["type"]] += 1
        
        # Process relations
        doc_relations = doc.get("labels", []) if "labels" in doc else doc.get("relations", [])
        total_relations += len(doc_relations)
        
        # Extract relation types
        for relation in doc_relations:
            rel_type = relation.get("r", relation.get("relation", "unknown"))
            relation_types[rel_type] += 1
        
        # Process sentences
        sents = doc.get("sents", [])
        total_sents += len(sents)
        total_tokens += sum(len(sent) for sent in sents)
    
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
    if not counter:
        print(f"Warning: No data to plot for {title}")
        return
        
    # Get the top 10 items or all if less than 10
    most_common = counter.most_common(10)
    if not most_common:
        print(f"Warning: Counter is empty for {title}")
        return
        
    labels, values = zip(*most_common)  # Get top 10
    
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
    entity_most_common = stats['entity_types'].most_common(5)
    if entity_most_common:
        for entity_type, count in entity_most_common:
            print(f"  - {entity_type}: {count}")
    else:
        print("  No entity types found")
    
    print("\nTop 5 relation types:")
    relation_most_common = stats['relation_types'].most_common(5)
    if relation_most_common:
        for relation_type, count in relation_most_common:
            print(f"  - {relation_type}: {count}")
    else:
        print("  No relation types found")

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
            if stats['entity_types']:
                plot_distribution(
                    stats['entity_types'], 
                    f'Entity Type Distribution ({split})',
                    results_dir / f"{split}_entity_types.png"
                )
            
            if stats['relation_types']:
                plot_distribution(
                    stats['relation_types'], 
                    f'Relation Type Distribution ({split})',
                    results_dir / f"{split}_relation_types.png"
                )
    
    print("\nAnalysis complete. Plots saved to the 'results' directory.")

if __name__ == "__main__":
    main()

