1. Project Folder Structure:
(php code)

vapt-as-a-service/
├── app.py                  # Main application logic
├── templates/              # HTML templates folder
│   └── index.html          # HTML file for frontend
├── static/                 # Static files (CSS)
│   └── style.css           # Styling for the frontend
├── reports/                # Folder where generated reports will be stored
├── requirements.txt        # List of dependencies
2. requirements.txt
Use this file to specify the dependencies needed to run the project:

(bash code)

Flask
nmap
nikto
sqlmap
reportlab
To install these dependencies, run:

(bash code)

pip install -r requirements.txt

3. app.py (Main Flask Application)
This is the backend logic of the application that runs the scans and generates PDF reports.
nano app.py
(python code)

from flask import Flask, render_template, request
import nmap
import subprocess
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Function to run Nmap scan
def run_nmap(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')  # Scanning ports 1 to 1024
    return nm.all_hosts(), nm.csv()

# Function to run Nikto scan
def run_nikto(target):
    result = subprocess.run(['nikto', '-h', target], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

# Function to run SQLMap scan
def run_sqlmap(target):
    result = subprocess.run(['sqlmap', '-u', target, '--batch', '--risk=3', '--level=5'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

# Function to generate PDF report
def generate_pdf(report, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 10)
    width, height = letter

    text = c.beginText(40, height - 40)
    text.textLines(report)
    c.drawText(text)
    c.showPage()
    c.save()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Result route to process the scan and generate report
@app.route('/scan', methods=['POST'])
def scan():
    if request.method == 'POST':
        target = request.form['target']
        # Run Nmap, Nikto, and SQLMap
        nmap_hosts, nmap_report = run_nmap(target)
        nikto_report = run_nikto(target)
        sqlmap_report = run_sqlmap(target)

        # Generate the report content
        report = f"Nmap Scan Results:\n{nmap_report}\n\nNikto Scan Results:\n{nikto_report}\n\nSQLMap Scan Results:\n{sqlmap_report}"
        
        # Save PDF report
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        report_filename = f"reports/vapt_report_{timestamp}.pdf"
        generate_pdf(report, report_filename)

        # Return the report to the user
        return render_template('index.html', target=target, report=report_filename)

if __name__ == '__main__':
    app.run(debug=True)

4. templates/index.html (Frontend HTML)
This file creates the user interface for submitting URLs/IPs for scanning and downloading the generated report.
nano  templates/index.html 
(html code)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAPT-as-a-Service</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>VAPT-as-a-Service Platform</h1>
        <form action="/scan" method="POST">
            <label for="target">Enter URL/IP for Scan:</label>
            <input type="text" id="target" name="target" required>
            <button type="submit">Start Scan</button>
        </form>

        {% if report %}
            <h2>Scan Report</h2>
            <p>Download your scan report <a href="{{ url_for('static', filename=report) }}">here</a></p>
        {% endif %}
    </div>
</body>
</html>
5. static/style.css (Frontend Styling)
This file provides basic styling for the frontend form.
nano  static/style.cs
(css code)

body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    padding: 50px;
}

.container {
    width: 60%;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 30px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #333;
}

form {
    margin-bottom: 20px;
    text-align: center;
}

input[type="text"] {
    padding: 10px;
    width: 60%;
    margin-right: 10px;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
6. Folder for Storing Reports
Make sure to create a folder named reports/ in your project directory to store the generated PDF reports.

(bash code)

mkdir reports

7. Setting Up the Application
Install Dependencies: Make sure you have the required libraries installed:

(bash code)

pip install -r requirements.txt
Run the Flask Application: Start the Flask application by running:

(bash code)

python app.py

Access the Application: Open a browser and go to http://127.0.0.1:5000/. You’ll see a simple form where you can input a URL or IP address for scanning.

8. Running the Vulnerability Scans
When you enter a URL or IP and submit the form, the following scans are executed:

Nmap: This tool performs a network scan and checks for open ports.
Nikto: This tool performs a web server scan and checks for known vulnerabilities.
SQLMap: This tool checks for SQL injection vulnerabilities on the provided target.
The results of all scans will be compiled into a PDF report and saved in the reports/ folder.
After the scan is complete, a link to download the generated PDF report will appear on the page.

9. Important Considerations
Permissions: Make sure you have permission to run these scans on the target (URL/IP). Unauthorized penetration testing can be illegal.

Dependencies: Ensure that the necessary tools (Nmap, Nikto, SQLMap) are installed on your machine and available in the system's PATH.

Summary of the Code

Backend: Flask app handles the scanning logic and PDF report generation.
Frontend: Simple HTML form to accept a URL/IP and display the download link for the report.
Reports: Generated as PDF files, stored in the reports/ folder, and available for download.
This should cover all the necessary details for your VAPT-as-a-Service Platform project. Let me know if you need any further help or modifications!








