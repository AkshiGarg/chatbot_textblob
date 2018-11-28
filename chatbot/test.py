from textblob import TextBlob

query_parameters = {}


def processNounPhrases(noun_phrases):
    count = 0;
    while count < len(noun_phrases) and noun_phrases[count] and noun_phrases[count].lower() != 'entrance door' and noun_phrases[count].lower() != 'reception area':
        count = count + 1
    query_parameters['resource_name'] = noun_phrases[count]


def processNoun(word):
    print(word)
    if word == 'morning' or word == 'evening' or word == 'afternoon' or word == 'night':
        query_parameters['time'] = word
    elif word == 'gym' or word == 'garage' or word == 'pool':
        query_parameters['resource_name'] = word


text = input('Hi, What do you want to know?');

blob = TextBlob(text)

processNounPhrases(blob.noun_phrases)

for word, tag in blob.pos_tags:
    # print(word + " " + tag)
    if tag == 'NN' or tag == 'NNS':
        processNoun(word.lower())

print(query_parameters)
