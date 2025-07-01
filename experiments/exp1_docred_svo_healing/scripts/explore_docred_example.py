#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DocRED Dataset Example Explorer

This script displays detailed examples from the DocRED dataset, showing:
1. A full document with its title, sentences, entities, and relations
2. How entities are linked to sentences
3. The actual relation information between entities

Original DocRED Dataset:
- Repository: https://github.com/thunlp/DocRED
- Paper: "DocRED: A Large-Scale Document-Level Relation Extraction Dataset"
- Authors: Yuan Yao, Deming Ye, Peng Li, Xu Han, Yankai Lin, Zhenghao Liu, Zhiyuan Liu, Lixin Huang, Jie Zhou, Maosong Sun
- Publication: ACL 2019
"""

import json
import os
from pathlib import Path
import random
import sys
import textwrap
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# ANSI color mapping for entity types
ENTITY_COLORS = {
    "LOC": Fore.GREEN,
    "PER": Fore.BLUE,
    "ORG": Fore.MAGENTA,
    "TIME": Fore.YELLOW,
    "MISC": Fore.CYAN,
    "NUM": Fore.WHITE + Style.BRIGHT,
    "default": Fore.WHITE
}

def load_json(file_path):
    """Load a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def load_relation_info(file_path):
    """Load relation info mapping relation IDs to names."""
    rel_info = load_json(file_path)
    if rel_info:
        # The rel_info.json file is already a dictionary mapping
        # relation IDs to their names, so we can return it directly
        return rel_info
    return {}

def get_dataset_paths():
    """Get paths to dataset files."""
    # Navigate to the data directory (assuming script is in scripts/ directory)
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent / "data"
    raw_data_dir = data_dir / "raw_data"
    
    dataset_files = {
        "train": raw_data_dir / "train_annotated.json",
        "dev": raw_data_dir / "dev.json",
        "test": raw_data_dir / "test.json",
        "rel_info": raw_data_dir / "rel_info.json"
    }
    
    # Check if files exist
    for split, path in dataset_files.items():
        if not path.exists():
            print(f"Warning: {split} file not found at {path}")
    
    return dataset_files

def reconstruct_document_text(sents):
    """Reconstruct the document text from sentences."""
    return " ".join([" ".join(sent) for sent in sents])

def display_document_text(sents, title=None):
    """Display the document text with sentence numbers."""
    if title:
        print(f"\n{Fore.CYAN + Style.BRIGHT}DOCUMENT: {title}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW + Style.BRIGHT}FULL TEXT:{Style.RESET_ALL}")
    
    # Combine sentences into paragraph for natural reading
    full_text = reconstruct_document_text(sents)
    for line in textwrap.wrap(full_text, width=100):
        print(f"  {line}")
    
    print(f"\n{Fore.YELLOW + Style.BRIGHT}TEXT BY SENTENCES:{Style.RESET_ALL}")
    for i, sent in enumerate(sents):
        sent_text = " ".join(sent)
        print(f"  {Fore.YELLOW}[Sentence {i}]{Style.RESET_ALL} {sent_text}")

def get_entity_color(entity_type):
    """Get ANSI color for entity type."""
    return ENTITY_COLORS.get(entity_type, ENTITY_COLORS["default"])

def display_entities(vertex_set):
    """Display entities with their mentions in the text."""
    print(f"\n{Fore.GREEN + Style.BRIGHT}ENTITIES:{Style.RESET_ALL}")
    
    for i, entity in enumerate(vertex_set):
        # Get entity type from first mention
        entity_type = entity[0].get("type", "UNKNOWN")
        entity_color = get_entity_color(entity_type)
        
        # Get entity name from first mention
        entity_name = entity[0].get("name", "UNKNOWN")
        
        print(f"  {entity_color + Style.BRIGHT}Entity {i} [{entity_type}]: {entity_name}{Style.RESET_ALL}")
        
        # Display mentions
        for j, mention in enumerate(entity):
            sent_id = mention.get("sent_id", -1)
            pos = mention.get("pos", [])
            if pos:
                pos_str = f"{pos[0]}:{pos[1]}"
            else:
                pos_str = "unknown"
            
            print(f"    {Fore.WHITE}Mention {j}: Sentence {sent_id}, Position {pos_str}")

def display_relations(labels, vertex_set, relation_info):
    """Display relations between entities with detailed information."""
    if not labels:
        print(f"\n{Fore.RED + Style.BRIGHT}NO RELATIONS FOUND IN THIS DOCUMENT{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.BLUE + Style.BRIGHT}RELATIONS:{Style.RESET_ALL}")
    
    for i, relation in enumerate(labels):
        head_id = relation.get("h", -1)
        tail_id = relation.get("t", -1)
        rel_id = relation.get("r", "unknown")
        
        # Get entity names if available
        head_name = "unknown"
        tail_name = "unknown"
        head_type = "unknown"
        tail_type = "unknown"
        
        if 0 <= head_id < len(vertex_set) and vertex_set[head_id]:
            head_name = vertex_set[head_id][0].get("name", "unknown")
            head_type = vertex_set[head_id][0].get("type", "unknown")
        
        if 0 <= tail_id < len(vertex_set) and vertex_set[tail_id]:
            tail_name = vertex_set[tail_id][0].get("name", "unknown")
            tail_type = vertex_set[tail_id][0].get("type", "unknown")
        
        # Get relation name from relation info
        rel_name = relation_info.get(rel_id, rel_id)
        
        head_color = get_entity_color(head_type)
        tail_color = get_entity_color(tail_type)
        
        print(f"  {Fore.BLUE + Style.BRIGHT}Relation {i}:{Style.RESET_ALL}")
        print(f"    {head_color}Entity {head_id} [{head_type}]: {head_name}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE + Style.BRIGHT}→ {rel_name} ({rel_id}) →{Style.RESET_ALL}")
        print(f"    {tail_color}Entity {tail_id} [{tail_type}]: {tail_name}{Style.RESET_ALL}")

def display_entity_sentence_links(vertex_set, sents):
    """Display how entities are linked to sentences with context."""
    print(f"\n{Fore.MAGENTA + Style.BRIGHT}ENTITY SENTENCE LINKS:{Style.RESET_ALL}")
    
    entity_to_sentences = {}
    
    # Collect entity mentions by sentence
    for entity_id, entity in enumerate(vertex_set):
        entity_name = entity[0].get("name", "UNKNOWN")
        entity_type = entity[0].get("type", "UNKNOWN")
        
        for mention in entity:
            sent_id = mention.get("sent_id", -1)
            if sent_id < 0 or sent_id >= len(sents):
                continue
                
            pos = mention.get("pos", [])
            if not pos or len(pos) < 2:
                continue
                
            if sent_id not in entity_to_sentences:
                entity_to_sentences[sent_id] = []
                
            entity_to_sentences[sent_id].append({
                "entity_id": entity_id,
                "entity_name": entity_name,
                "entity_type": entity_type,
                "start": pos[0],
                "end": pos[1]
            })
    
    # Display sentences with entity mentions highlighted
    for sent_id in sorted(entity_to_sentences.keys()):
        if sent_id >= len(sents):
            continue
            
        sentence = sents[sent_id]
        entity_mentions = entity_to_sentences[sent_id]
        
        print(f"  {Fore.YELLOW}[Sentence {sent_id}]{Style.RESET_ALL}")
        
        # Display original sentence
        original_text = " ".join(sentence)
        print(f"    Original: {original_text}")
        
        # Display sentence with entity mentions highlighted
        print(f"    With entities:")
        
        # Build token-level entity mapping
        token_entities = {}
        for mention in entity_mentions:
            start = mention["start"]
            end = mention["end"]
            for pos in range(start, end):
                if pos not in token_entities:
                    token_entities[pos] = []
                token_entities[pos].append(mention)
        
        # Construct highlighted text
        highlighted_parts = []
        for i, token in enumerate(sentence):
            if i in token_entities:
                # This token is part of an entity
                for mention in token_entities[i]:
                    entity_color = get_entity_color(mention["entity_type"])
                    entity_id = mention["entity_id"]
                    entity_type = mention["entity_type"]
                    start = mention["start"]
                    end = mention["end"]
                    
                    # Only process if this is the start of the entity mention
                    if i == start:
                        entity_text = " ".join(sentence[start:end])
                        highlighted_parts.append(f"{entity_color}[E{entity_id}:{entity_type}]{entity_text}{Style.RESET_ALL}")
                        # Skip the rest of this entity's tokens
                        break
            else:
                # Regular token not part of any entity
                highlighted_parts.append(token)
        
        # Display highlighted text
        highlighted_text = " ".join(highlighted_parts)
        # Wrap the text for better readability
        for line in textwrap.wrap(highlighted_text, width=100):
            print(f"      {line}")
        print()

def explore_document(doc, relation_info):
    """Explore a document in detail."""
    title = doc.get("title", "Untitled")
    sents = doc.get("sents", [])
    vertex_set = doc.get("vertexSet", [])
    labels = doc.get("labels", [])
    
    # Display document text
    display_document_text(sents, title)
    
    # Display entities
    display_entities(vertex_set)
    
    # Display relations
    display_relations(labels, vertex_set, relation_info)
    
    # Display entity-sentence links
    display_entity_sentence_links(vertex_set, sents)

def main():
    """Main function to explore DocRED dataset examples."""
    print(f"{Fore.CYAN + Style.BRIGHT}DocRED Dataset Example Explorer{Style.RESET_ALL}")
    print("=================================")
    print(f"Original dataset by Yuan Yao et al., ACL 2019")
    print(f"Repository: https://github.com/thunlp/DocRED")
    print("=================================\n")
    
    # Get dataset paths
    dataset_files = get_dataset_paths()
    
    # Load relation info
    relation_info = load_relation_info(dataset_files["rel_info"])
    if not relation_info:
        print("Warning: Could not load relation info mapping.")
    
    # Choose which split to explore
    split_choices = {"1": "train", "2": "dev", "3": "test"}
    print("Choose a dataset split to explore:")
    print("  1. Training set")
    print("  2. Development set")
    print("  3. Test set")
    
    split_choice = input("Enter your choice (1-3): ").strip()
    if split_choice not in split_choices:
        print("Invalid choice. Using training set by default.")
        split_choice = "1"
    
    split_name = split_choices[split_choice]
    dataset_path = dataset_files[split_name]
    
    # Load the dataset
    print(f"Loading {split_name} dataset...")
    data = load_json(dataset_path)
    if not data:
        print(f"Failed to load {split_name} dataset.")
        return
    
    print(f"Successfully loaded {len(data)} documents.")
    
    # Choose how to select a document
    print("\nHow would you like to select a document?")
    print("  1. Random document")
    print("  2. Specific document by index")
    
    selection_choice = input("Enter your choice (1-2): ").strip()
    
    doc_index = 0
    if selection_choice == "1":
        doc_index = random.randint(0, len(data) - 1)
        print(f"Selected random document at index {doc_index}.")
    elif selection_choice == "2":
        max_index = len(data) - 1
        try:
            doc_index = int(input(f"Enter document index (0-{max_index}): ").strip())
            if doc_index < 0 or doc_index > max_index:
                print(f"Invalid index. Using document 0 instead.")
                doc_index = 0
        except ValueError:
            print("Invalid input. Using document 0 instead.")
            doc_index = 0
    else:
        print("Invalid choice. Using a random document.")
        doc_index = random.randint(0, len(data) - 1)
    
    # Explore the selected document
    selected_doc = data[doc_index]
    print(f"\nExploring document at index {doc_index}...")
    explore_document(selected_doc, relation_info)
    
    print("\nExploration complete!")

if __name__ == "__main__":
    main()

