from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


app = Flask(__name__)


# Firebase objects init
# substitua o nome do arquivo .json a seguir pela chave .json que você baixou
# do console do Firebase
cred = credentials.Certificate("bookdevopsml1-b01e3-firebase-adminsdk-mb0zm-be785d786f.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
messages_ref = db.collection('messages')


@app.route('/messages', methods=['GET'])
def messages():
    result = []
    for message in list(messages_ref.get()):
        result.append(message.to_dict())
    n = len(result)
    response = {
        "n_result": n,
        "result": result
    }
    return jsonify(response)
