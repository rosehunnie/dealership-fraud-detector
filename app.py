from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_fraud(df):
    """
    Analyze the accounting data for potential fraud indicators
    Returns a dictionary of detected anomalies
    """
    anomalies = {
        'duplicate_transactions': [],
        'unusual_amounts': [],
        'suspicious_patterns': []
    }
    
    try:
        # Check for duplicate transactions
        duplicates = df[df.duplicated(subset=['transaction_id', 'amount', 'date'], keep=False)]
        if not duplicates.empty:
            anomalies['duplicate_transactions'] = duplicates.to_dict('records')
        
        # Check for unusual amounts (using z-score)
        if 'amount' in df.columns:
            df['z_score'] = np.abs((df['amount'] - df['amount'].mean()) / df['amount'].std())
            unusual = df[df['z_score'] > 3]
            if not unusual.empty:
                anomalies['unusual_amounts'] = unusual.to_dict('records')
        
        # Check for suspicious patterns (e.g., round numbers, frequent transactions)
        if 'amount' in df.columns:
            round_numbers = df[df['amount'] % 100 == 0]
            if not round_numbers.empty:
                anomalies['suspicious_patterns'].extend(round_numbers.to_dict('records'))
    except Exception as e:
        logger.error(f"Error in fraud detection: {str(e)}")
        raise
    
    return anomalies

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logger.info(f"File saved successfully: {filename}")
            
            try:
                # Read the file based on its extension
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                
                # Detect fraud
                anomalies = detect_fraud(df)
                
                return jsonify({
                    'message': 'File processed successfully',
                    'anomalies': anomalies
                })
                
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True) 