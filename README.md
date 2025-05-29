# 🛡️ Python Security Projects Collection

A curated collection of Python-based cybersecurity projects, tools, and scripts designed for learning, experimentation, and ethical hacking.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Tools-critical?style=for-the-badge&logo=shield&logoColor=white)
![MIT License](https://img.shields.io/github/license/yourusername/python-security-projects?style=for-the-badge)

---

## 🔍 About

This repository is a personal and educational portfolio of various security-focused Python scripts and mini-projects. Each subdirectory contains a separate tool or demonstration aimed at different aspects of cybersecurity including:

- Network analysis
- Vulnerability scanning
- Password cracking (ethical use)
- Malware detection (simulation)
- Log monitoring
- Encryption & hashing
- Threat intelligence APIs

---

## 🧪 Projects Included

| Project | Description |
|--------|-------------|
| **🔐 password-cracker/** | Brute-force password cracker for ZIP files and SHA hashes (educational only). |
| **🌐 port-scanner/**     | Multithreaded port scanner with banner grabbing. |
| **📡 network-sniffer/**  | Real-time packet capture using `scapy`. |
| **🧬 malware-sandbox/**  | Simulated static analysis tool for malware files. |
| **📈 log-analyzer/**     | Log file analyzer with regex-based threat detection. |
| **🔑 rsa-encryption/**   | Simple RSA key generation and encryption demo. |
| **🕸️ subdomain-finder/**| Enumerates subdomains using wordlists and DNS lookups. |
| **📬 email-spam-detector/** | Basic machine learning classifier for spam detection. |

---

## 🛠 Requirements

- Python 3.7+
- `pip install -r requirements.txt` inside each project folder
- Some tools may require admin/root access (e.g., network sniffing)

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. Please use all tools responsibly and **only on systems you own or have permission to test**.

---

## 📦 How to Use

```bash
# Clone the repository
git clone https://github.com/yourusername/python-security-projects.git

# Navigate into a project folder
cd port-scanner

# Install requirements
pip install -r requirements.txt

# Run the tool
python scanner.py
