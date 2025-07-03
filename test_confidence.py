#!/usr/bin/env python3
"""
Test script to demonstrate confidence calculation with Z-score normalization.
This script loads triples, calculates confidence scores, and shows the before/after values.
"""

import sys
import pandas as pd
from src.confidence_calculator import ConfidenceCalculator

def main():
    # Load triples
    print("Loading triples from data/mini_static.csv...")
    try:
        df = pd.read_csv("data/mini_static.csv")
        triples = df.to_dict('records')
    except Exception as e:
        print(f"Error loading triples: {e}")
        sys.exit(1)
    
    # Store original confidence values
    original_confidences = {}
    for i, triple in enumerate(triples):
        key = f"{triple['s']}-{triple['p']}-{triple['o']}"
        original_confidences[key] = float(triple.get('confidence', 1.0))
    
    # Calculate new confidence scores
    print("\nCalculating confidence scores using Z-score normalization...")
    calculator = ConfidenceCalculator()
    updated_triples = calculator.calculate_scores(triples)
    
    # Print results
    print("\nResults (original vs. calculated confidence):")
    print("-" * 80)
    print(f"{'Subject':<15} {'Predicate':<15} {'Object':<20} {'Original':<10} {'Calculated':<10} {'Diff':<10}")
    print("-" * 80)
    
    for triple in updated_triples:
        key = f"{triple['s']}-{triple['p']}-{triple['o']}"
        original = original_confidences[key]
        calculated = float(triple['confidence'])
        diff = calculated - original
        
        print(f"{triple['s']:<15} {triple['p']:<15} {triple['o']:<20} {original:<10.2f} {calculated:<10.2f} {diff:+.2f}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("-" * 40)
    orig_vals = list(original_confidences.values())
    calc_vals = [float(t['confidence']) for t in updated_triples]
    
    print(f"Original confidence: min={min(orig_vals):.2f}, max={max(orig_vals):.2f}, avg={sum(orig_vals)/len(orig_vals):.2f}")
    print(f"Calculated confidence: min={min(calc_vals):.2f}, max={max(calc_vals):.2f}, avg={sum(calc_vals)/len(calc_vals):.2f}")
    
    # Explain weights used
    print("\nWeights used in calculation:")
    print("-" * 40)
    for key, value in calculator.weights.items():
        print(f"{key}: {value:.2f}")
    
    print("\nTo adjust these weights, edit config/confidence_weights.yaml")

if __name__ == "__main__":
    main()
