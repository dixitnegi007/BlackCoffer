import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, cmudict
from string import punctuation
import re
import os

# Function to extract text from URL
def extract_article_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_text = ""
    # Extract only the article title and text
    title = soup.title.text if soup.title else ""
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        article_text += paragraph.text + "\n"
    return title, article_text

# Read input data
input_df = pd.read_csv("Input.xlsx - Sheet1.csv")

# Extract text from URLs and save to files
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article_text = extract_article_data(url)
    with open(f"{url_id}.txt", 'w', encoding='utf-8') as file:
        file.write(title + "\n\n" + article_text)

# Initialize CMU Pronouncing Dictionary
pronouncing_dict = cmudict.dict()

# Load stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load positive and negative words
positive_words = set()
negative_words = set()

master_dict_dir = "MasterDictionary"
for filename in os.listdir(master_dict_dir):
    with open(os.path.join(master_dict_dir, filename), 'r', encoding='ISO-8859-1') as file:
        word_list = file.read().splitlines()
        if filename == 'positive-words.txt':
            positive_words.update(word for word in word_list if word.lower() not in stop_words)
        elif filename == 'negative-words.txt':
            negative_words.update(word for word in word_list if word.lower() not in stop_words)

# Define function to count syllables in a word
def count_syllables(word):
    if word.lower() in pronouncing_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in pronouncing_dict[word.lower()]])
    else:
        return 0

# Define function to remove stopwords and punctuation
def clean_text(text):
    words = word_tokenize(text)
    cleaned_words = [word.lower() for word in words if word.lower() not in stop_words and word not in punctuation]
    return cleaned_words

# Define function to calculate complexity metrics
def calculate_complexity_metrics(text):
    sentences = sent_tokenize(text)
    words = clean_text(text)
    num_words = len(words)
    num_sentences = len(sentences)
    
    # Average sentence length
    avg_sentence_length = num_words / num_sentences
    
    # Percentage of complex words
    complex_word_count = sum(1 for word in words if count_syllables(word) > 2)
    percentage_complex_words = (complex_word_count / num_words) * 100
    
    # Fog index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    return avg_sentence_length, percentage_complex_words, fog_index

# Define function to calculate personal pronouns count
def calculate_personal_pronouns(text):
    pattern = r'\b(I|we|my|ours|us)\b'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    # Filter out matches that are not related to the country name "US"
    matches = [match for match in matches if match.lower() != 'us']
    return len(matches)

# Perform analysis for each article
output_data = []
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    with open(f"{url_id}.txt", 'r', encoding='utf-8') as file:
        article_text = file.read()
    
    # Sentiment analysis
    words = clean_text(article_text)
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / max((positive_score + negative_score), 1)
    subjectivity_score = (positive_score + negative_score) / max(len(words), 1)
    
    # Complexity metrics
    avg_sentence_length, percentage_complex_words, fog_index = calculate_complexity_metrics(article_text)
    
    # Other metrics
    word_count = len(words)
    complex_word_count = sum(1 for word in words if count_syllables(word) > 2)
    syllable_per_word = sum(count_syllables(word) for word in words) / max(word_count, 1)
    personal_pronouns = calculate_personal_pronouns(article_text)
    avg_word_length = sum(len(word) for word in words) / max(word_count, 1)
    
    output_data.append([url_id, positive_score, negative_score, polarity_score, subjectivity_score,
                        avg_sentence_length, percentage_complex_words, fog_index, word_count,
                        complex_word_count, syllable_per_word, personal_pronouns, avg_word_length])

# Create output DataFrame
output_df = pd.DataFrame(output_data, columns=['URL_ID', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 
                                               'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 
                                               'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 
                                               'WORD COUNT', 'COMPLEX WORD COUNT', 
                                               'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 
                                               'AVG WORD LENGTH'])

# Save output to Excel
output_df.to_excel("Output.xlsx", index=False)
