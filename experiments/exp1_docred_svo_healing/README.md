# DocRED Dataset Implementation

## Dataset Source and Attribution

This implementation uses the DocRED (Document-Level Relation Extraction Dataset) from the original work:

* **Original Repository**: [https://github.com/thunlp/DocRED](https://github.com/thunlp/DocRED)
* **Paper**: *"DocRED: A Large-Scale Document-Level Relation Extraction Dataset"*
* **Authors**: Yuan Yao, Deming Ye, Peng Li, Xu Han, Yankai Lin, Zhenghao Liu, Zhiyuan Liu, Lixin Huang, Jie Zhou, Maosong Sun
* **Publication**: ACL 2019

## Dataset Description

DocRED is a large-scale document-level relation extraction dataset that was constructed from Wikipedia and Wikidata. It contains:
- Documents annotated with named entities and their relations
- Rich semantic features
- Both direct and indirect relation mentions
- Complex reasoning patterns

## Directory Structure

- `data/`: Contains the DocRED dataset files
- `scripts/`: Implementation code for processing and using the dataset
- `results/`: Directory for storing experiment outputs

## Acknowledgments

We express our gratitude to the original DocRED authors and contributors for making this valuable dataset publicly available. This implementation builds upon their work for research purposes.

## License

The original DocRED dataset and code are licensed under their respective terms. Please refer to the original repository for detailed licensing information.
