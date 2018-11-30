from textblob import TextBlob
from sql_builder import SqlBuilder
from db_utils import DBUtils


class ChatBot:
    allowed_resources = ['entrance door', 'reception area', 'pool', 'gym', 'garage']
    allowed_times = ['morning', 'evening', 'afternoon', 'night']

    sql_builder = None
    db_utils = None

    def __init__(self):
        self.sql_builder = SqlBuilder()
        self.db_utils = DBUtils()

    def process_question(self, question):
        query_parameters = {}
        blob = TextBlob(question)
        noun_phrases = blob.noun_phrases
        if len(noun_phrases) > 0:
            self.process_noun_phrases(noun_phrases, query_parameters)
        for word, tag in blob.pos_tags:
            if tag == 'NN' or tag == 'NNS':
                self.process_noun(word.lower(), query_parameters)
            self.column_name(query_parameters, word)

        while 'column' not in query_parameters.keys():
            text = input("Looking for a count or people? ['How many'/'Who']")
            self.column_name(query_parameters, text.lower())

        while 'resource_name' not in query_parameters.keys():
            text = input("Where do you want to look?? {0}\n".format(self.allowed_resources))
            if text.lower() in self.allowed_resources:
                query_parameters['resource_name'] = text.lower()

        query = self.sql_builder.build_query(column=query_parameters['column'],
                                             resource_name=query_parameters['resource_name'],
                                             time_identifier=query_parameters[
                                                 'time'] if 'time' in query_parameters.keys() else None)
        result = self.db_utils.query(query)
        if query_parameters['column'].__contains__('count'):
            print("Total of ", result[0][0])
        else:
            print("It's ", ', '.join(str(r[0]) for r in result))

    def column_name(self, query_parameters, word):
        if word.lower().__contains__('how'):
            query_parameters['column'] = 'count(*)'
        if word.lower().__contains__('who'):
            query_parameters['column'] = 'distinct(credential_holder_name)'

    def process_noun_phrases(self, noun_phrases, query_parameters):
        count = 0
        while count < len(noun_phrases) and noun_phrases[count] and noun_phrases[count].lower() != 'entrance door':
            count = count + 1
        query_parameters['resource_name'] = noun_phrases[count]

    def process_noun(self, word, query_parameters):
        if word.lower() in self.allowed_times:
            query_parameters['time'] = word
        elif word.lower() in self.allowed_resources:
            query_parameters['resource_name'] = word


bot = ChatBot()

text = input('Hi, Do you want to know anything?\n')

while text.lower() != 'n' or text.lower() != 'no':
    bot.process_question(text)
    text = input('Anything else?\n')

print("Thank You !!")
