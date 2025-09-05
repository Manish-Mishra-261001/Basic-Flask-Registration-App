from flask import Flask,request,jsonify
from dotenv import load_dotenv
import os
import pymongo


load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
db = client.flask_todo_DB
collection = db['flask_todo_collection']

app = Flask(__name__)

@app.route('/submittodoitem',methods=['POST'])
def submit():
    backend_itemName=request.form.get('itemName')
    backend_itemDescription=request.form.get('itemDescription')
    dictionary_form=dict(request.json)    
    if(backend_itemName=='' or backend_itemDescription==''):
        return 'Item Name or Description Cannot be blank.'
    else:
        collection.insert_one(dictionary_form)
        return 'Data Submitted Successfully'

@app.route('/view')
def view():
    data = collection.find()
    list_data = list(data)
    for item in list_data:
        print(item)
        del item['_id']
    dictionary_data = {
        'data': list_data
    }
    return jsonify(dictionary_data)

if __name__ == '__main__':
 app.run(host='0.0.0.0',port=9000,debug=True)
