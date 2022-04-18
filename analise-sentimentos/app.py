from unicodedata import category
from classificador.model import Model
from kafka import KafkaConsumer
import json
import pickle
# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Conecta o classificador ao Kafka, em servidor local, no tópico "chatbot"
consumer = KafkaConsumer('chatbot', bootstrap_servers='localhost:9092')

# Firebase objects init
# substitua o nome do arquivo .json a seguir pela chave .json que você baixou
# do console do Firebase
cred = credentials.Certificate("bookdevopsml1-b01e3-firebase-adminsdk-mb0zm-be785d786f.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
messages_ref = db.collection('messages')


# Carrega o classificador de categorias
print('Carregando classificador de categorias...')
category_model = pickle.load(open('model.sav', 'rb'))
print('Classificador carregado!')

# Carrega o modelo BERT pré-treinado (demora um tempinho)
print('Carregando modelo...')
model = Model(category_model)
print('Modelo carregado!')

# Enquanto houver mensagens, analisa o sentimento
for msg in consumer:
    obj = json.loads(msg.value)
    # sentiment, confidence, probabilities = model.predict(obj['pergunta'])
    sentiment, confidence, probabilities, category = model.predict(obj['pergunta'])
    sentimento = ':|'
    if sentiment == 'negative':
        sentimento = ':('
    elif sentiment == 'positive':
        sentimento = ':)'
    print (sentimento + ' ' + obj['nome']+' disse '+obj['pergunta'] + " | " + "recognized product category: " + category)
    messages_ref.add(
        {
            "name": obj['nome'],
            "message": obj['pergunta'],
            "category": category,
            "sentiment": sentiment
        }
    )
    if sentiment == 'negative':
        print('Atendente humano, converse com o usuário '+obj['nome']+' na sessão '+obj['sessao']+"! Rápido!")
