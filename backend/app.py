from flask import Flask,request,jsonify
from dotenv import load_dotenv
import os
import pymongo


load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
db = client.flask_Assigment_DB             
collection = db['flask_Assigment_collection']

app = Flask(__name__)

@app.route('/submit',methods=['POST'])
def submit():
    backend_password=request.form.get('password')
    backend_confirm_password=request.form.get('confirm_password')
    dictionary_form=dict(request.json)    
    if(backend_password=='' or backend_confirm_password==''):
        return 'Password or confirm Password Cannot be blank.'
    else:
        if (backend_password==backend_confirm_password):
            collection.insert_one(dictionary_form)
            return 'Data Submitted Successfully'
        else:
            return "Registration failed!!! Due to mismatch between password and confirm password."

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
