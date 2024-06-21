import spacy
from spacy.matcher import Matcher
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# Load your text from a file
with open('sampletext.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Define the sentiment analysis classifier
def classify_sentiment_vader(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return 'In Favor'
    elif scores['compound'] <= -0.05:
        return 'Against'
    else:
        return 'Neutral'

# Custom keyword classifier
def classify_based_on_keywords(text):
    in_favor_keywords = ['support', 'endorse', 'back', 'favor', 'advocate', 'approve', 'commend', 'uphold', 'promote', 'recommend', 'embrace', 'champion', 'defend', 'affirm']
    against_keywords = ['oppose', 'against', 'reject', 'object', 'condemn', 'criticize', 'deny', 'refuse', 'dispute', 'contest', 'dissent', 'rebut', 'renounce', 'resist']


    text = text.lower()
    favor_count = sum(1 for word in in_favor_keywords if word in text)
    against_count = sum(1 for word in against_keywords if word in text)

    if favor_count > against_count:
        return 'In Favor'
    elif against_count > favor_count:
        return 'Against'
    else:
        return 'Neutral'

def classify_statement(text):
    sentiment_class = classify_sentiment_vader(text)
    keyword_class = classify_based_on_keywords(text)

    if sentiment_class == keyword_class:
        return sentiment_class
    elif sentiment_class == 'Neutral':
        return keyword_class
    elif keyword_class == 'Neutral':
        return sentiment_class
    else:
        # If there is a conflict between sentiment and keyword classification, keyword classification takes precedence
        return keyword_class
    
# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

def extract_statements(text, speaker_title, speaker_name):
    # Process the text with spaCy
    doc = nlp(text)
    
    # Initialize the matcher with the shared vocab
    matcher = Matcher(nlp.vocab)
    
    # Define the pattern to find the mention of the speaker's title and name
    pattern = [
        {"LOWER": speaker_title.lower()},  # Title (Ms., Mr., etc.) in lowercase
        {"IS_PUNCT": True, "OP": "?"},     # Optional punctuation
        {"LOWER": speaker_name.lower()}    # Speaker's last name in lowercase
    ]
    matcher.add("SPEAKER_PATTERN", [pattern])
    
    # Use the matcher on the doc
    matches = matcher(doc)
    
    # Extract and return the statements
    statements = []
    for match_id, start, end in matches:
        # Extract the matched span
        span = doc[start:end]
        current_sentence = span.sent
        full_statement = current_sentence.text

        # Continue to the next sentence if it does not contain a new speaker
        # Skip "Mr. Speaker" as it does not denote a change in speaker
        next_sentence = doc[current_sentence.end:].sent
        while next_sentence:
            if next_sentence.text.startswith(("Mr.", "Ms.", "Dr.")) and not "Mr. Speaker" in next_sentence.text:
                break
            full_statement += " " + next_sentence.text
            if next_sentence.end >= len(doc):
                break
            next_sentence = doc[next_sentence.end:].sent

        statements.append(full_statement)
    
    return statements



def classify_vote(text, speaker_name):
    """
    Search for a speaker's name in the voting section of the text and classify their vote.

    Parameters:
        text (str): The text containing the voting results.
        speaker_name (str): The full name or last name of the speaker to search for.

    Returns:
        str: The voting classification ('Yea', 'Nay', or 'Not Found' if the speaker did not vote).
    """
    # Normalize the speaker name to ensure consistent casing
    speaker_name = speaker_name.lower()

    # Normalize the text to ensure consistent casing and split into lines
    lines = text.lower().split('\n')
    
    # Initialize variables to determine the current section of the text
    processing_yeas = False
    processing_nays = False
    
    # Iterate through each line
    for line in lines:
        # Identify the current section based on keywords
        if 'yeas--' in line:
            processing_yeas = True
            processing_nays = False
        elif 'nays--' in line:
            processing_yeas = False
            processing_nays = True
        elif 'not voting--' in line:
            processing_yeas = False
            processing_nays = False

        # Search for the speaker's name in the appropriate section
        if processing_yeas and speaker_name in line:
            return 'Yea'
        elif processing_nays and speaker_name in line:
            return 'Nay'

    # Return 'Not Found' if the speaker's name is not found in either section
    return 'Not Found'

##### Nancy Pelosi #####

speaker_title = "Ms."
speaker_name = "Pelosi"
statements = extract_statements(text, speaker_title, speaker_name)

# Print the extracted statements
# for statement in statements:
#     print(f"Extracted statement: {statement}")

# save to pelosi_statements.txt
with open('pelosi_statements.txt', 'w') as file:
    for statement in statements:
        file.write(statement + '\n')


for statement in statements:
    classification = classify_statement(statement)
    print(f"Statement: {statement}\nClassification: {classification}")

speaker_name = 'Pelosi'  # Correct name to search for
vote_result = classify_vote(text, speaker_name)
print(f"{speaker_name} voted: {vote_result}")


##### Kevin McCarthy #####
speaker_title = "Mr."
speaker_name = "McCarthy"
statements = extract_statements(text, speaker_title, speaker_name)

# Print the extracted statements
# for statement in statements:
#     print(f"Extracted statement: {statement}")

# save to mccarthy_statements.txt
with open('mccarthy_statements.txt', 'w') as file:
    for statement in statements:
        file.write(statement + '\n')


for statement in statements:
    classification = classify_statement(statement)
    print(f"Statement: {statement}\nClassification: {classification}")


speaker_name = 'McCarthy'  # Correct name to search for
vote_result = classify_vote(text, speaker_name)
print(f"{speaker_name} voted: {vote_result}")


##### John Boehner ##### Does The speaker vote?
speaker_title = "Speaker"
speaker_name = "Boehner"
statements = extract_statements(text, speaker_title, speaker_name)

# Print the extracted statements
# for statement in statements:
#     print(f"Extracted statement: {statement}")

# save to boehner_statements.txt
with open('boehner_statements.txt', 'w') as file:
    for statement in statements:
        file.write(statement + '\n')


for statement in statements:
    classification = classify_statement(statement)
    print(f"Statement: {statement}\nClassification: {classification}")

speaker_name = 'Boehner'  # Correct name to search for
vote_result = classify_vote(text, speaker_name)
print(f"{speaker_name} voted: {vote_result}")

