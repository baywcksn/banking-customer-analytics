# 🟢 Milestone 1 — Project Planning & Setup

## 1. Purpose

Milestone ini bertujuan untuk menentukan arah proyek, ruang lingkup analisis, business questions, kebutuhan data, teknologi yang digunakan, serta menyiapkan environment proyek agar proses berikutnya dapat dilakukan secara terstruktur dan reproducible.

---

## 2. Business Problem

Bank memiliki data customer, account, product, dan transaction dalam jumlah besar. Data tersebut dapat digunakan untuk memahami perilaku nasabah, aktivitas transaksi, penggunaan produk, performa channel, serta pola customer dari waktu ke waktu.

Masalah utama yang ingin dijawab melalui proyek ini adalah bagaimana mengubah data operasional tersebut menjadi informasi yang dapat digunakan untuk memahami customer behavior dan transaction performance.

---

## 3. Business Questions

Analisis akan berfokus pada beberapa pertanyaan:

1. Bagaimana volume dan nilai transaksi berubah dari waktu ke waktu?
2. Bagaimana karakteristik dan pola aktivitas customer?
3. Produk banking apa yang paling banyak digunakan?
4. Bagaimana performa transaksi berdasarkan channel?
5. Seberapa baik customer kembali bertransaksi setelah transaksi pertama?
6. Bagaimana customer dapat dikelompokkan menggunakan RFM?
7. Pola apa yang dapat menjadi indikasi potential churn?

---

## 4. Data Requirements

Data yang dibutuhkan meliputi:

* Customer information
* Account information
* Product information
* Transaction information
* Account balance history

Relasi utama:

```text
CUSTOMER
   │
   │ 1:N
   ▼
ACCOUNT
   ├── N:1 → PRODUCT
   ├── 1:N → TRANSACTION
   └── 1:N → BALANCE HISTORY
```

---

## 5. Analytical Scope

Analisis mencakup:

* Transaction performance
* Customer analytics
* Product analytics
* Channel analytics
* Customer retention
* Cohort analysis
* RFM segmentation
* Churn analysis
* Dashboard dan business insights

Analisis diarahkan untuk menghasilkan insight yang dapat dijelaskan secara kuantitatif dan memiliki hubungan dengan business questions.

---

## 6. Technology Stack

### Core

* Python
* SQL
* PostgreSQL
* Git
* GitHub

### Data Transformation

* dbt

### Data Analysis

* Pandas
* NumPy
* Matplotlib

### Visualization

* Power BI

### Infrastructure

* Docker

Airflow bersifat optional dan hanya digunakan jika memang memberikan manfaat terhadap workflow analitik.

---

## 7. Project Architecture

Workflow proyek:

```text
Data Sources
      ↓
Python Ingestion
      ↓
PostgreSQL
      ↓
dbt Transformation
      ↓
Analytical Data Marts
      ↓
SQL Analysis
      ↓
Python Analysis
      ↓
Power BI
      ↓
Business Insights
```

Pendekatan ini memisahkan proses ingestion, storage, transformation, analysis, visualization, dan business communication.

---

## 8. Project Setup

Project dibuat menggunakan struktur dasar:

```text
banking-customer-analytics/
├── data/
├── notebooks/
├── sql/
├── src/
├── docs/
├── dashboard/
├── README.md
├── .gitignore
└── .venv/
```

Python virtual environment dibuat menggunakan `.venv` agar dependency proyek terisolasi dari environment Python sistem.

Git repository juga telah dibuat dan dihubungkan dengan repository GitHub:

`banking-customer-analytics`

---

## 9. Guiding Principles

### Business First

Analisis dimulai dari business questions, bukan sekadar eksplorasi kolom.

### Data Quality

Data harus diperiksa sebelum digunakan sebagai dasar insight.

### Reproducibility

Proses analisis harus dapat dijalankan kembali dengan workflow dan kode yang terdokumentasi.

### Separation of Concerns

Raw data, transformation, analysis, dan visualization dipisahkan agar workflow lebih mudah dipelihara.

### Evidence-Based Insights

Insight harus didukung oleh data dan perhitungan yang dapat ditelusuri.

### Professional Documentation

Setiap tahap penting dalam proyek didokumentasikan agar mudah dipahami dan direview kembali.

---

## 10. Milestone Checklist

* [x] Define project scope
* [x] Define business problem
* [x] Define business questions
* [x] Define data requirements
* [x] Define analytical scope
* [x] Define technology stack
* [x] Define project architecture
* [x] Define project principles
* [x] Create project directory
* [x] Initialize Git repository
* [x] Install Python
* [x] Create virtual environment
* [x] Create GitHub repository
* [x] Synchronize local repository with GitHub
* [ ] Push project documentation

---

## 11. Milestone Output

Milestone 1 menghasilkan:

* Project scope
* Business problem
* Business questions
* Data requirements
* Analytical scope
* Technology stack
* Project architecture
* Guiding principles
* Initial project structure
* Git dan GitHub repository
* Python virtual environment

Milestone berikutnya adalah **Milestone 2 — Data Collection & Understanding**.