from chatterbot import ChatBot

chatbot = ChatBot('NoVaci', trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer')

# chatbot.train('chatterbot.corpus.vietnamese')

print(chatbot.get_response("lát qua đón"))
