# Accounting Fraud Detection System

A modern web application for detecting potential fraud in accounting files. The system analyzes uploaded accounting files for various anomalies and suspicious patterns.

## Features

- Upload CSV or Excel files containing accounting data
- Automatic detection of:
  - Duplicate transactions
  - Unusual amounts (using statistical analysis)
  - Suspicious patterns (e.g., round numbers)
- Modern, responsive user interface
- Real-time analysis and results display

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Setup

### Backend Setup

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask backend:
```bash
python app.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Drag and drop an accounting file (CSV or Excel) or click to select a file
3. Wait for the analysis to complete
4. Review the detected anomalies in the results table

## File Format

The system expects accounting files with the following columns:
- transaction_id
- amount
- date
- description (optional)
- category (optional)

## Contributing

Feel free to submit issues and enhancement requests! 