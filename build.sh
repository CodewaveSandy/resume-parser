#!/bin/bash
echo "Downloading nltk models..."
python -m nltk.downloader stopwords punkt averaged_perceptron_tagger wordnet maxent_ne_chunker words

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm
