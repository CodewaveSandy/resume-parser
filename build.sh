#!/bin/bash

# Install all Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK resources
python -m nltk.downloader stopwords punkt averaged_perceptron_tagger wordnet maxent_ne_chunker words

# Download spaCy model
python -m spacy download en_core_web_sm
