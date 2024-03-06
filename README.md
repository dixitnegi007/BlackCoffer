# BlackCoffer

Approach:

This Python script aims to perform text analysis and data extraction based on the provided requirements. The approach involves several steps:

Data Extraction:

The script extracts textual data articles from the URLs provided in the Input.xlsx file. It utilizes the requests library to fetch HTML content from each URL and then uses BeautifulSoup for parsing HTML to extract the article title and text.
Extracted data is saved to text files with filenames corresponding to the URL_ID.
Text Analysis:

Sentiment Analysis: Utilizes positive and negative word dictionaries from the Master Dictionary folder to calculate positive score, negative score, polarity score, and subjectivity score for each article.
Complexity Metrics: Calculates average sentence length, percentage of complex words, and Fog index to analyze the readability of the text.
Other Metrics: Computes word count, complex word count, syllable per word, personal pronouns count, and average word length.
All computed metrics are then stored in an output DataFrame.
Dependencies:

pandas: Used for data manipulation and DataFrame operations.
requests: Required for fetching HTML content from URLs.
BeautifulSoup: Utilized for parsing HTML content and extracting article text.
nltk: Used for natural language processing tasks such as tokenization, stop word removal, and syllable counting.
Running the Script:

To generate the output, follow these steps:

Make sure you have Python installed on your system.
Install the required dependencies by running the following command:
Copy code:
pip install pandas requests beautifulsoup4 nltk os


pip install pandas requests beautifulsoup4 nltk
Place the input Excel file (Input.xlsx), Master Dictionary folder, and the Python script (text_analysis.py) in the same directory.
Run the Python script by executing the following command in your terminal or command prompt:
Copy code:
python text_analysis.py


Once the script completes execution, it will generate an output Excel file named Output.xlsx containing the analyzed data.


Note: Ensure that you have an active internet connection while running the script to fetch data from URLs.

Author: Dixit Negi

Contact: dixitnegi007@gmail.com 

Date: 07-03-2024






