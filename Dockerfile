FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y gcc

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords punkt averaged_perceptron_tagger wordnet maxent_ne_chunker words
RUN python -m spacy download en_core_web_sm

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:$PORT", "app:app"]
