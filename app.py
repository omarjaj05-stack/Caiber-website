from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    company = data.get('company')
    topic = data.get('topic')
    message = data.get('message')
    
    # You can save this to a database or send an email
    print(f"Form submitted: Name={name}, Email={email}, Company={company}, Topic={topic}, Message={message}")
    
    return jsonify({'status': 'success', 'message': 'Form submitted successfully!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
