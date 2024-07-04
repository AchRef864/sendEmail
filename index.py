from flask import Flask, request, jsonify
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Generate OTP function
def generate_otp():
    return ''.join(random.choices('0123456789', k=5))

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()  # Get JSON data from the request
    if not data or 'email' not in data:
        return jsonify({'error': 'Email parameter is required'}), 400

    recipient_email = data['email']
    otp = generate_otp()

    # SMTP server configuration (example using Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'rahaliashraf732@gmail.com'  # Replace with your Gmail email address
    sender_password = 'tmij cpbn afud lkwu'  # Replace with your Gmail password

    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Your OTP Code'

    body = f'Your OTP code is: {otp}'
    message.attach(MIMEText(body, 'plain'))

    # Send email via SMTP
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return jsonify({'message': 'OTP sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
