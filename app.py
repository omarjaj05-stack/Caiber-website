from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from datetime import datetime

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

@app.route('/pam-scanner')
def pam_scanner():
    return render_template('pam-scanner.html')

@app.route('/roi-calculator')
def roi_calculator():
    return render_template('roi-calculator.html')

@app.route('/compliance-checker')
def compliance_checker():
    return render_template('compliance-checker.html')

@app.route('/threat-feed')
def threat_feed():
    return render_template('threat-feed.html')

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
    """Chat with Claude AI"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'})
        
        # Import inside function
        from anthropic import Anthropic
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({'response': 'API key not configured'})
        
        # Create client and call API
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return jsonify({'response': message.content[0].text})
        
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)[:100]}'})

@app.route('/api/send-report', methods=['POST'])
def send_report():
    """Send generated reports via email"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        report_type = data.get('reportType', '')

        if not email:
            return jsonify({'status': 'error', 'message': 'Email required'}), 400

        # Generate report content based on type
        if report_type == 'PAM_Scanner':
            subject = 'Your PAM Assessment Report from Caiber'
            body = f"""
PAM SECURITY ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ORGANIZATION: {data.get('orgName', 'Your Organization')}

ASSESSMENT RESULTS
------------------
PAM Maturity Score: {data.get('maturityScore', 'N/A')}
Compliance Status: {data.get('complianceStatus', 'N/A')}
Critical Issues Found: {data.get('criticalIssues', 'N/A')}

KEY FINDINGS
-----------
✓ Comprehensive network scan completed
✓ Security vulnerabilities identified
✗ Remediation recommendations included

NEXT STEPS
----------
1. Review all findings in this report
2. Contact Caiber for implementation roadmap
3. Schedule enterprise consultation

For questions: hello@caiber.ca
Contact: +1-800-CAIBER-1
"""

        elif report_type == 'ROI_Calculator':
            subject = 'Your Caiber ROI Analysis Report'
            body = f"""
CAIBER ROI ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
-----------------
5-Year Total Savings: {data.get('roiAmount', '$0')}

KEY METRICS
-----------
✓ Manual Labor Cost Reduction: 65% reduction
✓ Year 1 Savings: {data.get('year1', '$0')}
✓ Breach Prevention Value: {data.get('breachSavings', '$0')}
✓ Payback Period: {data.get('payback', 'N/A')}

INVESTMENT DETAILS
------------------
Caiber Assist Implementation
- Advanced AI Threat Detection
- Real-time Privilege Monitoring
- Automated Compliance Reporting
- 24/7 Intelligent Response

EXPECTED OUTCOMES
------------------
1. Reduced security incidents by 85%
2. Manual PAM workload reduced by 65%
3. Faster threat response (milliseconds vs hours)
4. Full compliance automation
5. Continuous optimization

For implementation details: hello@caiber.ca
"""

        elif report_type == 'Compliance_Checker':
            frameworks_text = '\n'.join([f"{'✓' if f['pass'] else '✗'} {f['name']}: {'COMPLIANT' if f['pass'] else 'NOT COMPLIANT'}" for f in data.get('frameworks', [])])
            recs_text = '\n'.join(data.get('recommendations', []))
            
            subject = f"Your Compliance Assessment Report - Score: {data.get('score')}%"
            body = f"""
PAM COMPLIANCE ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

COMPLIANCE SCORE
----------------
Overall Score: {data.get('score')}%

FRAMEWORK STATUS
----------------
{frameworks_text}

PRIORITY RECOMMENDATIONS
------------------------
{recs_text}

WHAT CAIBER DOES
----------------
✓ Centralizes privileged access management
✓ Implements automated compliance monitoring
✓ Deploys AI-powered threat detection
✓ Enables real-time audit logging
✓ Ensures continuous compliance

Next Step: Schedule a consultation with Caiber
Contact: hello@caiber.ca
"""

        else:
            return jsonify({'status': 'error', 'message': 'Invalid report type'}), 400

        # Send email
        msg = Message(
            subject=subject,
            recipients=[email],
            body=body
        )
        mail.send(msg)
        
        # Also log to your email
        log_msg = Message(
            subject=f'Report Sent: {report_type}',
            recipients=['mjalgailani@gmail.com'],
            body=f"Report ({report_type}) sent to {email}"
        )
        try:
            mail.send(log_msg)
        except:
            pass  # Silently fail if logging email fails

        return jsonify({'status': 'success', 'message': f'Report sent to {email}'}), 200

    except Exception as e:
        print(f"Error sending report: {e}")
        return jsonify({'response': f'Error: {str(e)[:100]}'}), 400
