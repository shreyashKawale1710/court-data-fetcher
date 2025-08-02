# Court-Data Fetcher & Mini-Dashboard

## Description
A web app to fetch and display metadata and judgments for cases from the Delhi High Court. Built with Flask and SQLite.

## Features
- Inputs: Case Type, Case Number, Filing Year
- Parses parties, filing date, next hearing, and latest judgment PDF
- Logs all queries and raw HTML responses in a local database
- Simple frontend UI with error handling

## Court Targeted
Delhi High Court — https://delhihighcourt.nic.in/

## CAPTCHA Handling
Currently not enforced. If introduced later, manual token or third-party CAPTCHA-solving services may be used.

## Setup Instructions
```bash
pip install -r requirements.txt
python app.py
```

## Deliverables
- app.py - Flask backend
- templates/ - HTML UI
- README.md - documentation
- requirements.txt - dependencies

## License
MIT
