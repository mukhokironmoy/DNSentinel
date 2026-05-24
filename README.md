# DNS Exfiltration Detection System

DNS Exfiltration Detection System is a cybersecurity and machine learning project that detects DNS tunneling activity in network traffic. DNS tunneling is a covert channel technique where attackers encode stolen data inside DNS queries, usually by placing long, random-looking encoded payloads inside subdomains. This project is designed to identify such suspicious DNS behavior using protocol-level DNS parsing, feature engineering, classical machine learning, deep learning, and a live dashboard.

## Tech Stack

- Python
- scikit-learn
- Keras
- Streamlit
- SQLite

## Demo

To be filled in after M-8.

## Results

To be filled in after M-7.

## Quick Start

To be filled in after M-8.

## Repository Structure

```text
dns-exfil-detector/
├── dns_server/
│   ├── server.py
│   ├── parser.py
│   ├── forwarder.py
│   └── logger.py
├── pipeline/
│   ├── features.py
│   ├── dataset.py
│   └── scorer.py
├── models/
│   ├── phase1_classical.ipynb
│   ├── phase2_autoencoder.ipynb
│   └── phase3_lstm_cnn.ipynb
├── dashboard/
│   └── app.py
├── attack_sim/
│   └── tunnel_sim.py
├── tests/
│   └── test_parser.py
├── data/
│   └── download.sh
├── demo/
├── requirements.txt
└── README.md