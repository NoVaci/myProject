from chatterbot import ChatBot

chatbot = ChatBot('NoVaci', trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer')

# chatbot.train('chatterbot.corpus.vietnamese')
while (True):
    ask = input('ToKo: ')
    if ask == 'exit':
        break
    else:
        print("Little Tily: " + str(chatbot.get_response(ask)))
