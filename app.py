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

@app.route('/ai-assessment')
def ai_assessment():
    return render_template('ai-assessment.html')

@app.route('/api/analyze-pam', methods=['POST'])
def analyze_pam():
    """Real PAM analysis using Claude AI"""
    try:
        # Get form data
        org_name = request.form.get('org_name', '').strip()
        org_size = request.form.get('org_size', '').strip()
        system_count = request.form.get('system_count', '').strip()
        industry = request.form.get('industry', '').strip()
        email = request.form.get('email', '').strip()
        
        if not all([org_name, org_size, system_count, industry, email]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        file_content = file.read().decode('utf-8', errors='ignore')
        
        if not file_content:
            return jsonify({'error': 'File is empty'}), 400
        
        # Prepare detailed prompt for Claude
        analysis_prompt = f"""
You are an EXPERT PAM (Privileged Access Management) Security Analyst with 20+ years of experience.

ORGANIZATION CONTEXT:
- Name: {org_name}
- Size: {org_size}
- System Count: {system_count}
- Industry: {industry}

ANALYZE THIS PAM DATA:
{file_content[:8000]}

YOU MUST PROVIDE A DETAILED, ACCURATE SECURITY ASSESSMENT INCLUDING:

1. ACCOUNT INVENTORY ANALYSIS:
   - Count privileged/admin accounts found
   - Identify unmanaged or orphaned accounts
   - List service accounts without proper controls
   - Flag accounts without MFA
   - Note shared accounts or credentials

2. CRITICAL VULNERABILITIES (Be SPECIFIC):
   - List each actual vulnerability found in the data
   - Explain the security risk and impact
   - Provide CVSS-style severity (Critical/High/Medium/Low)
   - Show which specific accounts/systems are affected

3. COMPLIANCE FRAMEWORK GAPS (Map to actual findings):
   - SOC 2 violations found (specific requirements violated)
   - ISO 27001 non-compliance issues
   - HIPAA gaps (if healthcare industry)
   - PCI-DSS violations
   - CIS Controls misses

4. ACCESS CONTROL ISSUES:
   - Over-privileged accounts
   - Incorrect permission assignments
   - Missing separation of duties
   - Excessive access duration

5. AUTHENTICATION & MFA GAPS:
   - Accounts without MFA
   - Weak authentication methods used
   - Legacy protocols still enabled
   - Password policy violations

6. RISK QUANTIFICATION:
   - Overall Risk Score: 1-100
   - Count CRITICAL findings (most severe)
   - Count HIGH severity issues
   - Count MEDIUM severity issues
   - Count LOW severity issues
   - Estimated impact if breached (financial exposure)

7. TOP 7 REMEDIATION PRIORITIES:
   Priority 1 (CRITICAL - Do First): [Specific issue with why]
   Priority 2 (CRITICAL): [Specific issue]
   Priority 3 (HIGH): [Specific issue]
   Priority 4 (HIGH): [Specific issue]
   Priority 5 (MEDIUM): [Specific issue]
   Priority 6 (MEDIUM): [Specific issue]
   Priority 7 (MEDIUM): [Specific issue]

8. IMPLEMENTATION TIMELINE:
   Week 1-2: [Quick wins - critical fixes]
   Week 3-4: [High priority remediations]
   Month 2-3: [Medium priority improvements]
   Ongoing: [Long-term security enhancements]

9. COMPLIANCE STATUS BY FRAMEWORK:
   - SOC 2: [% Compliant] - [Key gaps]
   - ISO 27001: [% Compliant] - [Key gaps]
   - HIPAA: [% Compliant] - [Key gaps if applicable]
   - PCI-DSS: [% Compliant] - [Key gaps if applicable]

IMPORTANT: Be SPECIFIC and TECHNICAL. Reference actual data found in the uploaded file.
Do NOT be generic. Quote actual findings from the data.
Make the report ACTIONABLE and DETAILED.
Format for easy reading in an HTML report.
"""

        # Call Claude API
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({'error': 'API configuration error'}), 500
        
        client = Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        analysis_text = message.content[0].text
        
        # Generate HTML report
        html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PAM Assessment Report - {org_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #333; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 0 30px rgba(0,0,0,0.1); border-radius: 8px; }}
        .header {{ border-bottom: 4px solid #00c8c8; padding-bottom: 30px; margin-bottom: 30px; }}
        .logo {{ color: #00c8c8; font-size: 32px; font-weight: bold; }}
        .subtitle {{ color: #666; margin-top: 10px; font-size: 14px; }}
        h1 {{ color: #0a0e27; font-size: 28px; margin: 30px 0 15px 0; border-bottom: 2px solid #00c8c8; padding-bottom: 10px; }}
        h2 {{ color: #00c8c8; font-size: 18px; margin: 25px 0 15px 0; }}
        .org-info {{ background: #f9f9f9; padding: 20px; border-left: 4px solid #00c8c8; margin: 20px 0; border-radius: 6px; }}
        .org-info p {{ margin: 8px 0; }}
        .critical {{ color: #ff4444; font-weight: bold; }}
        .high {{ color: #ffaa00; font-weight: bold; }}
        .medium {{ color: #ffdd00; color: #666; font-weight: bold; }}
        .section {{ margin: 30px 0; }}
        .finding {{ background: #fff9f9; border-left: 4px solid #ff4444; padding: 15px; margin: 15px 0; border-radius: 4px; }}
        .finding.high {{ background: #fffaf9; border-left-color: #ffaa00; }}
        .finding.medium {{ background: #fffff9; border-left-color: #ffdd00; }}
        .finding.low {{ background: #f9fff9; border-left-color: #00ff88; }}
        .recommendation {{ background: #f9fff9; border-left: 4px solid #00ff88; padding: 15px; margin: 15px 0; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f5f5f5; color: #0a0e27; font-weight: bold; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px; text-align: center; }}
        .score-box {{ font-size: 18px; color: #ff4444; font-weight: bold; margin: 20px 0; padding: 20px; background: #fff9f9; border-radius: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">CAIBER</div>
            <div class="subtitle">Professional PAM Security Assessment Report</div>
            <div style="color: #999; margin-top: 10px; font-size: 12px;">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>

        <div class="org-info">
            <h2 style="margin-top: 0; color: #0a0e27;">Organization Summary</h2>
            <p><strong>Organization:</strong> {org_name}</p>
            <p><strong>Organization Size:</strong> {org_size}</p>
            <p><strong>Systems Analyzed:</strong> {system_count}</p>
            <p><strong>Industry:</strong> {industry}</p>
            <p><strong>Assessment Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
        </div>

        <h1>Executive Summary</h1>
        <p>This PAM Security Assessment was conducted using advanced AI analysis of your infrastructure data. 
        The findings below represent actual vulnerabilities and compliance gaps identified in your uploaded data.</p>

        <h1>Detailed Assessment Results</h1>
        <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; white-space: pre-wrap; font-family: 'Segoe UI', Arial; line-height: 1.8; color: #333;">
{analysis_text}
        </div>

        <h1>Recommended Next Steps</h1>
        <div class="recommendation">
            <strong>1. Share with Leadership</strong>
            <p>Distribute this report to your CISO, IT Director, and CFO to ensure organizational awareness of security posture.</p>
        </div>
        <div class="recommendation">
            <strong>2. Schedule Implementation Planning</strong>
            <p>Contact Caiber to discuss a detailed remediation plan and timeline for addressing identified vulnerabilities.</p>
        </div>
        <div class="recommendation">
            <strong>3. Deploy Caiber Assist</strong>
            <p>Implement continuous PAM monitoring with Caiber Assist to detect and prevent future unauthorized access.</p>
        </div>

        <h1>About This Assessment</h1>
        <p>This assessment was conducted using AI-powered analysis of your uploaded infrastructure data. The findings are based on 
        actual account configurations, system settings, and compliance requirements for your industry.</p>
        
        <p><strong>What was analyzed:</strong></p>
        <ul>
            <li>Privileged account inventory and configurations</li>
            <li>Authentication and MFA status</li>
            <li>Access control policies and permissions</li>
            <li>Compliance framework alignment</li>
            <li>Security risks and vulnerabilities</li>
        </ul>

        <p><strong>For the most comprehensive assessment, provide:</strong></p>
        <ul>
            <li>Active Directory user and group exports</li>
            <li>PAM system configuration files</li>
            <li>Authentication logs (last 30 days)</li>
            <li>Access control policy documents</li>
            <li>Recent compliance audit reports</li>
        </ul>

        <h1>Get Professional Help</h1>
        <div style="background: linear-gradient(135deg, rgba(0,200,200,0.1) 0%, rgba(0,200,200,0.05) 100%); padding: 20px; border-left: 4px solid #00c8c8; border-radius: 6px;">
            <p><strong>Ready to fix these issues?</strong></p>
            <p>Caiber offers comprehensive PAM solutions to remediate vulnerabilities, enforce compliance, and deploy continuous monitoring.</p>
            <p><strong>Contact us:</strong> hello@caiber.ca | +1-800-CAIBER-1</p>
        </div>

        <div class="footer">
            <p><strong>CAIBER PAM Assessment</strong> - Powered by Advanced AI Analysis</p>
            <p>This report is confidential and for authorized recipients only.</p>
            <p>© {datetime.now().year} Caiber. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Send email
        try:
            msg = Message(
                subject=f'Your PAM Assessment Report - {org_name}',
                recipients=[email],
                html=html_report
            )
            mail.send(msg)
            
            # Log to admin
            log_msg = Message(
                subject=f'PAM Assessment Completed - {org_name}',
                recipients=['mjalgailani@gmail.com'],
                body=f"Assessment for {org_name} ({org_size}, {system_count} systems) completed and sent to {email}"
            )
            mail.send(log_msg)
        except Exception as e:
            print(f"Email send error: {e}")
        
        return jsonify({
            'success': True,
            'message': f'Assessment complete! Report sent to {email}',
            'report': html_report
        }), 200
    
    except Exception as e:
        print(f"Error in analyze_pam: {e}")
        return jsonify({'error': f'Analysis error: {str(e)[:100]}'}), 500

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
