# Springer Capital – Data Engineer Take-Home Assignment

This project processes the referral program dataset and generates:
- A final referral validation report
- A profiling summary for all tables
- A business-friendly data dictionary
- A Docker-ready pipeline for automated execution


## 📂 Project Structure

springer_referral/
│
├── your_script.py
├── Dockerfile
├── requirements.txt
├── data_dictionary.xlsx
├── README.md
│
├── data/
│     ├─ lead_log.csv
│     ├─ paid_transactions.csv
│     ├─ referral_rewards.csv
│     ├─ user_logs.csv
│     ├─ user_referral_logs.csv
│     ├─ user_referral_statuses.csv
│     └─ user_referrals.csv
│
└── out/
      ├─ report.csv
      └─ profiling_summary.csv


## 📌 How to Run Locally

### 1️⃣ Install dependencies

### 2️⃣ Run the script

### 3️⃣ Output Files
- **out/report.csv** → Final validated referral report  
- **out/profiling_summary.csv** → Null count + distinct count profiling  


## 🐳 Run Inside Docker

### 1️⃣ Build Docker image

### 2️⃣ Run container

This will automatically generate:
- `/out/report.csv`
- `/out/profiling_summary.csv`


## 📘 File Descriptions

| File | Description |
|------|-------------|
| **your_script.py** | Main processing pipeline |
| **Dockerfile** | Container setup |
| **requirements.txt** | Project dependencies |
| **data_dictionary.xlsx** | Business descriptions of all columns |
| **out/profiling_summary.csv** | Data profiling summary |
| **out/report.csv** | Final referral validation output |


## ✅ Deliverables Included

- your_script.py  
- Dockerfile  
- requirements.txt  
- data_dictionary.xlsx  
- profiling_summary.csv  
- report.csv  
- README.md  


## ✔ Status

This project has been tested locally and in Docker. Outputs are generated successfully.

