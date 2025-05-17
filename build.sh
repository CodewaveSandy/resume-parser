#!/bin/bash

# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Download NLTK resources
python -m nltk.downloader stopwords punkt averaged_perceptron_tagger wordnet maxent_ne_chunker words

# Step 3: (Optional) Download a compatible spaCy model (for spaCy v2.3.9)
python -m spacy download en_core_web_sm

# Step 4: Mark as executable (run this locally just once)
# chmod +x build.sh