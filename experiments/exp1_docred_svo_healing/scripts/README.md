# DocRED Dataset Processing Scripts

This directory contains scripts for processing and exploring the DocRED dataset.

## Scripts:

- `data_processing/gen_data.py`: Script for generating processed dataset files
- `data_processing/evaluation.py`: Evaluation utilities for the dataset
- `explore_docred.py`: Dataset exploration and statistics generation

## Usage

1. First, ensure you have the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. To process the raw dataset:
   ```
   python data_processing/gen_data.py
   ```

3. To explore the dataset:
   ```
   python explore_docred.py
   ```

## Data Format

The DocRED dataset is provided in JSON format with the following structure:

```json
{
    "title": "Document title",
    "sents": [
        ["token1", "token2", ...],
        ...
    ],
    "entities": [
        {
            "name": "entity_name",
            "type": "entity_type",
            "pos": [[sent_id, start_pos, end_pos], ...]
        },
        ...
    ],
    "relations": [
        {
            "h": head_entity_id,
            "t": tail_entity_id,
            "r": relation_type
        },
        ...
    ]
}
```
