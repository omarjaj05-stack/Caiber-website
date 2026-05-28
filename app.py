from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-gmail@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'your-gmail@gmail.com')

mail = Mail(app)

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
    
    # Print to console
    print(f"Form submitted: Name={name}, Email={email}, Company={company}, Topic={topic}, Message={message}")
    
    # Send email to manager
    try:
        msg = Message(
            subject=f'New Caiber Service Inquiry from {name}',
            recipients=['mjalgailani@gmail.com'],
            body=f"""
New service inquiry from Caiber website:

Name: {name}
Email: {email}
Company: {company}
Service Type: {topic}
Message: {message}

---
Please respond to: {email}
            """
        )
        mail.send(msg)
        return jsonify({'status': 'success', 'message': 'Thank you! We will contact you within 24 hours.'})
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': 'Form submitted but there was an issue. We will still contact you.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
