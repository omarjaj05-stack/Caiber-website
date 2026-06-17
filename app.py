from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
import anthropic

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

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cyber-assist')
def cyber_assist():
    return render_template('cyber-assist.html')

@app.route('/cyber-implement')
def cyber_implement():
    return render_template('cyber-implement.html')

@app.route('/cyber-mature')
def cyber_mature():
    return render_template('cyber-mature.html')

@app.route('/ai-agent')
def ai_agent():
    return render_template('ai-agent.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        
        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        company = data.get('company', '').strip()
        topic = data.get('topic', '').strip()
        message = data.get('message', '').strip()
        
        # Check required fields
        if not name or not email or not topic:
            return jsonify({'status': 'error', 'message': 'Please fill in all required fields'}), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'status': 'error', 'message': 'Please enter a valid email'}), 400
        
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
            # Still return success since the data was received
            return jsonify({'status': 'success', 'message': 'Thank you! We will contact you within 24 hours.'}), 200
    except Exception as e:
        print(f"Error processing form: {e}")
        return jsonify({'status': 'error', 'message': 'There was an error. Please try again.'}), 400

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Chat with Claude AI for PAM security analysis"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        
        # System prompt for PAM expertise
        system_prompt = """You are an expert AI security agent for Caiber's Privileged Access Management (PAM) system. 
You specialize in:
- Real-time threat detection and analysis
- Privileged access monitoring
- Security compliance (SOC 2, ISO 27001, HIPAA, PCI-DSS)
- Policy optimization recommendations
- User behavior pattern analysis
- Incident response strategies

You are knowledgeable about:
- Access anomalies and suspicious behaviors
- Credential management best practices
- Multi-factor authentication requirements
- Least privilege principles
- Compliance requirements across industries

Always provide:
1. Direct, actionable insights
2. Specific recommendations with reasoning
3. Risk assessment when relevant
4. Enterprise-focused solutions

Keep responses concise but comprehensive (2-3 sentences for simple questions, more detail for complex scenarios)."""
        
        # Create message with Claude
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract response
        response_text = message.content[0].text
        
        return jsonify({
            'response': response_text,
            'status': 'success'
        })
    
    except Exception as e:
        print(f"AI Chat Error: {e}")
        return jsonify({
            'error': str(e),
            'response': 'I encountered an error processing your request. Please try again.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
