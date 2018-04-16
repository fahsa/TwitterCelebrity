import string
import re
import nltk

def feature_engineering(df):
    # Tokenize
    remove_punct = str.maketrans('','',string.punctuation)
    df['words'] = df['text'].apply(lambda text: nltk.word_tokenize(text.translate(remove_punct)))
    # Word count
    df['word_count'] = df['words'].apply(lambda words: len(words))
    # Average word length
    df['avg_word_length'] = df['words'].apply(lambda words: sum(len(word) for word in words)/len(words) if len(words) > 0 else 0)
    # Character count
    df['char_count'] = df['text'].apply(lambda text: len(text))
    # Repeated Characters
    test = re.compile(r'([a-zA-z])\1{2,}')
    df['rep_char_count'] = df['text'].apply(lambda text: sum(1 for _ in test.finditer(text)))
    # Capitalization
    df['caps_count'] = df['words'].apply(lambda words: sum([1 for word in words if word.isupper() and word != 'I']))
    # Ellipses (..) Count
    ellipses = re.compile("\.{2,}")
    df['ellipses'] = df['text'].apply(lambda text: sum(1 for _ in ellipses.finditer(text)))
    # Exclamation Mark Count
    df['!_count'] = df['text'].apply(lambda text: sum([1 for char in text if char == '!']))
    # Repeated Exclamation Mark (!!) Count
    repeated_exclamation = re.compile("\!{2,}")
    df['rep_!_count'] = df['text'].apply(lambda text: sum(1 for _ in repeated_exclamation.finditer(text)))
    # Question Mark Count
    df['?_count'] = df['text'].apply(lambda text: sum([1 for char in text if char == '?']))
    # Repeated Question Mark (??) Count
    repeated_question = re.compile("\?{2,}")
    df['rep_?_count'] = df['text'].apply(lambda text: sum(1 for _ in repeated_question.finditer(text)))
    # Feature vector for the above
    df['features'] = df[['word_count', 'avg_word_length', 'char_count', 'rep_char_count', 'caps_count', 'ellipses', '!_count', 'rep_!_count', '?_count', 'rep_?_count']].values.tolist()
    return df
