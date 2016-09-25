from config import API_URL
import utils
import spacy


class NlpEnglish:
    def __init__(self):
        print('----- Loading NLP -----')
        self.en_nlp = spacy.load('en')
        print('----- NLP loaded -----')

    def echo(self, bot, update):
        user_name, user_id, group = utils.get_info(update)
        text = update.message.text
        parsed_text = self.en_nlp(text)
        output = ''
        for token in parsed_text:
            output += token.orth_ + ' ' + token.pos_ + ' ' + token.lemma_ + '\n'

        if output:
            bot.sendMessage(group, text=output)
