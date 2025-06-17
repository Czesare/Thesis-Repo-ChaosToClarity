# AI Ticket Data Preprocessing & Augmentation

This repository contains preprocessing scripts used to prepare a ticket support dataset for classification and clustering models. It includes privacy filtering, text normalization (stemming & stopword removal), and data augmentation through backtranslation.

## Workflow Overview

All data first goes through:

1. **Privacy Filtering**  
   Run `privacy_filter.py` to remove sensitive data such as phone numbers, emails, and dates.

After privacy filtering, you can choose one of the following (optional) paths:

- **Text Normalization**  
  Run `stem_and_filter.py` to apply stemming and stopword removal. Useful before training models sensitive to word form or noise.

- **Data Augmentation**  
  Run `augment_backtranslation.py` to balance class distribution via Dutch → English → Dutch backtranslation.

> Note: Augmentation is not meant to be run on the stemmed set, 
> but stemming **can** be applied **after** augmentation if needed.



These scripts can be used independently or sequentially, depending on your preprocessing needs.

## File Descriptions

| File                     | Purpose                                           |
|--------------------------|---------------------------------------------------|
| `privacy_filter.py`      | Redacts personal information from the dataset     |
| `stem_and_filter.py`     | Applies stemming and stopword removal             |
| `augment_backtranslation.py` | Augments the training set via backtranslation  |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt

