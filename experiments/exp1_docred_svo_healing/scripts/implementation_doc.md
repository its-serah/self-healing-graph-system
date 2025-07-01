# DocRED Dataset Implementation Documentation

## 1. Project Overview
We implemented a system to explore and analyze the DocRED (Document-Level Relation Extraction Dataset) within the self-healing knowledge graph project. The implementation focuses on dataset exploration and processing, removing model training components to concentrate on data understanding.

## 2. Project Structure
Current working directory: /home/serah/Desktop/DocRED/experiments/exp1_docred_svo_healing/

### Directory Structure:
```
experiments/exp1_docred_svo_healing/
├── data/
│   ├── raw_data/              # Original DocRED dataset files
│   │   ├── train_annotated.json
│   │   ├── dev.json
│   │   ├── test.json
│   │   ├── rel_info.json
│   │   └── DocRED_baseline_metadata/
│   └── prepro_data/           # For preprocessed data
├── scripts/
│   ├── data_processing/       # Data processing utilities
│   │   ├── evaluation.py
│   │   └── gen_data.py
│   ├── explore_docred.py      # Dataset statistics script
│   └── explore_docred_example.py  # Interactive dataset explorer
├── results/                   # Generated visualizations
└── README.md                  # Project documentation
```

## 3. Technologies Used
1. **Programming Language**: Python 3
2. **Key Libraries**:
   - json: For handling JSON dataset files
   - colorama: For colored terminal output
   - matplotlib: For generating visualizations
   - numpy: For numerical operations
   - pathlib: For cross-platform path handling

## 4. Implementation Steps

### 4.1 Dataset Organization
1. Created the experiment structure under exp1_docred_svo_healing/
2. Set up separate directories for raw data, processed data, scripts, and results
3. Moved DocRED dataset files to raw_data/ directory

### 4.2 Data Processing Scripts
1. Created data_processing/ directory with:
   - evaluation.py: For dataset evaluation utilities
   - gen_data.py: For data generation and preprocessing

### 4.3 Dataset Exploration Tools
1. explore_docred.py:
   - Purpose: Generate dataset statistics and visualizations
   - Features:
     * Document count analysis
     * Entity and relation type distribution
     * Sentence and token statistics
     * Visualization generation

2. explore_docred_example.py:
   - Purpose: Interactive document explorer
   - Features:
     * Colored entity highlighting
     * Relation visualization
     * Entity-sentence linking
     * Document structure analysis

## 5. Data Format
The DocRED dataset uses JSON format with the following structure:
```json
{
    "title": "Document title",
    "sents": [["token1", "token2", ...], ...],
    "vertexSet": [
        [{"name": "entity_name", "type": "entity_type", "pos": [sent_id, start_pos, end_pos], ...}],
        ...
    ],
    "labels": [
        {"h": head_entity_id, "t": tail_entity_id, "r": relation_type},
        ...
    ]
}
```

## 6. Key Features Implemented

### 6.1 Entity Processing
- Entity type recognition (PER, LOC, ORG, TIME, MISC, NUM)
- Entity mention tracking across sentences
- Entity position mapping in text

### 6.2 Relation Processing
- Relation type mapping using rel_info.json
- Relation visualization between entities
- Bi-directional relation support

### 6.3 Text Processing
- Sentence-level tokenization
- Entity highlighting in context
- Cross-reference between entities and sentences

## 7. Visualization Features
1. Entity type distribution plots
2. Relation type distribution plots
3. Colored terminal output for:
   - Entity mentions
   - Relations between entities
   - Document structure

## 8. Technical Decisions

### 8.1 Code Organization
- Separated data processing from exploration tools
- Modular design for easy extension
- Clear separation of concerns between different script functionalities

### 8.2 Data Handling
- Raw data preserved in raw_data/
- Processing scripts in separate directory
- Results directory for generated artifacts

### 8.3 User Interface
- Interactive command-line interface
- Color-coded output for better readability
- Flexible document selection (random or specific)

## 9. Future Improvements
1. Add data validation tools
2. Implement data export features
3. Add more visualization options
4. Create batch processing capabilities

## 10. Usage Instructions
1. Dataset Exploration:
   ```bash
   python3 scripts/explore_docred.py
   ```
2. Interactive Document Analysis:
   ```bash
   python3 scripts/explore_docred_example.py
   ```

## 11. Dependencies
Required Python packages:
```
colorama
matplotlib
numpy
```
