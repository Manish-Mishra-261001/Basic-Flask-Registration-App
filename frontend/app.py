from flask import Flask,render_template,request, redirect, url_for, flash
import requests
import secrets
BACKEND_URL = 'http://127.0.0.1:9000'

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generates a secure random key
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    dictionary_data = dict(request.form)
    try:
        response = requests.post(BACKEND_URL + '/submit', json=dictionary_data, timeout=5)
#        response.raise_for_status()  # Raises HTTPError for 4xx/5xx status
    except requests.exceptions.RequestException as e:
        flash(f"Error submitting data: {str(e)}", "error")
        return render_template('index.html', form_data=dictionary_data)
    
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')  # This will show "Data submitted successfully"

@app.route('/api')
def api():
    response = requests.get(BACKEND_URL+'/view')
    response_data = response.json()
    response_data['api_context']='Registration_API'
    return response_data

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8000,debug=True)