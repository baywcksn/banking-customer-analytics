# 🟡 Milestone 2 — Data Collection & Understanding

## 1. Purpose

Milestone ini bertujuan untuk memperoleh dataset yang sesuai dengan kebutuhan analisis, memahami struktur data, mengetahui grain setiap tabel, memvalidasi hubungan antar tabel, serta melakukan profiling awal terhadap data.

Fokus utama tahap ini adalah **memahami data sebelum melakukan proses cleaning, transformation, dan analysis**.

---

## 2. Dataset Source

Dataset yang digunakan berasal dari **Banking Digital Twin** dan digenerate secara lokal menggunakan generator yang tersedia pada repository.

Konfigurasi dataset:

* Customers: 10,000
* Periode transaksi: 2023-01-01 hingga 2024-12-31
* Total seluruh file: 40 CSV
* Total rows: ±17.67 juta
* Ukuran dataset: ±3.08 GB
* Seed: 42

Walaupun dataset menyediakan banyak domain seperti fraud, lending, authentication, dan banking sessions, analisis utama menggunakan tabel yang relevan dengan scope proyek.

### Core Tables

1. `customer.csv`
2. `account.csv`
3. `product.csv`
4. `transaction.csv`
5. `account_balance_history.csv`

---

## 3. Core Tables & Grain

### Customer

**Grain:** satu baris merepresentasikan satu customer.

* Rows: 10,000
* Unique `customer_id`: 10,000
* Duplicate primary key: 0

Kolom yang relevan untuk analisis antara lain:

* `customer_id`
* `date_of_birth`
* `gender`
* `marital_status`
* `education_level`
* `region`
* `segment`
* `lifecycle_stage`
* `financial_literacy_score`
* `risk_appetite`
* `technology_adoption`
* `credit_score`
* `stress_score`
* `status`
* `onboarding_date`

---

### Account

**Grain:** satu baris merepresentasikan satu account.

* Rows: 25,316
* Unique `account_id`: 25,316
* Duplicate primary key: 0

Relationship:

`customer.customer_id → account.customer_id`

Setiap customer memiliki minimal 1 account dan maksimal 6 account.

Distribusi account per customer:

* 1 account: 840 customer
* 2 account: 4,348 customer
* 3 account: 3,633 customer
* 4 account: 1,022 customer
* 5 account: 149 customer
* 6 account: 8 customer

Rata-rata: **2.53 account/customer**.

---

### Product

**Grain:** satu baris merepresentasikan satu product.

* Rows: 86
* Unique `product_id`: 86
* Duplicate primary key: 0

Relationship:

`product.product_id → account.product_id`

Product digunakan untuk menganalisis penggunaan produk per customer maupun aktivitas transaksi berdasarkan produk.

---

### Transaction

**Grain:** satu baris merepresentasikan satu transaksi finansial.

* Rows: 7,610,818
* Unique `transaction_id`: 7,610,818
* Duplicate primary key: 0
* Periode: 2023-01-01 sampai 2024-12-31

Relationship:

`account.account_id → transaction.account_id`

Transaction merupakan **fact utama** dalam analisis karena menyediakan informasi aktivitas transaksi, nilai transaksi, waktu, channel, transaction type, dan atribut lainnya.

---

### Account Balance History

**Grain:** satu baris merepresentasikan histori saldo sebuah account pada suatu periode.

* Rows: 607,584
* Unique account: 25,316
* Unique `history_id`: 607,584
* Periode: 2023-01-01 sampai 2024-12-01
* Setiap account memiliki 24 records

Kolom utama:

* `account_id`
* `balance_date`
* `opening_balance`
* `closing_balance`
* `min_balance`
* `max_balance`

Tabel ini digunakan untuk analisis perkembangan saldo dari waktu ke waktu.

---

## 4. Relationship & Data Integrity

Struktur utama dataset:

```text
CUSTOMER
   │
   │ 1:N
   ▼
ACCOUNT
   ├── N:1 → PRODUCT
   │
   ├── 1:N → TRANSACTION
   │
   └── 1:N → BALANCE HISTORY
```

Hasil relationship check:

| Relationship          | Orphan Records |
| --------------------- | -------------: |
| Account → Customer    |              0 |
| Account → Product     |              0 |
| Transaction → Account |              0 |

Hasil tersebut menunjukkan bahwa foreign key utama pada core dataset memiliki referential integrity yang baik.

---

## 5. Initial Data Profiling

### Customer

Total customer: **10,000**

Segment:

* MASS: 4,959
* MASS_AFFLUENT: 2,010
* AFFLUENT: 1,117
* STUDENT: 945
* SENIOR: 739
* HNW: 230

Lifecycle stage:

* FAMILY_FORMATION: 2,039
* RETIRED: 2,034
* ESTABLISHED: 2,019
* YOUNG_PROFESSIONAL: 1,970
* PRE_RETIREMENT: 1,938

Technology adoption:

* EARLY_MAJORITY: 3,559
* LATE_MAJORITY: 2,938
* EARLY_ADOPTER: 1,514
* LAGGARD: 1,510
* INNOVATOR: 479

Gender:

* M: 4,911
* F: 4,895
* NB: 194

Semua customer berstatus `ACTIVE`.

---

### Account

Total account: **25,316**

Account type:

* CURRENT_ACCOUNT: 10,000
* SAVINGS: 8,016
* CREDIT_CARD: 3,955
* PERSONAL_LOAN: 1,329
* MORTGAGE: 1,246
* INVESTMENT: 770

Semua account pada profiling awal berstatus `ACTIVE` dan menggunakan currency `GBP`.

---

### Transaction

Total transaksi: **7,610,818**

Nilai transaksi:

* Minimum: 0.32
* Maximum: 28,521.51
* Total: 1,373,815,202.76
* Average: 180.51

Direction:

* DEBIT: 7,270,818 (95.53%)
* CREDIT: 340,000 (4.47%)

Channel:

* POS: 5,807,522
* ONLINE: 1,097,636
* ATM: 365,660
* BATCH: 340,000

Transaction type:

* CONTACTLESS: 3,761,881
* PURCHASE: 2,923,621
* ATM_WITHDRAWAL: 365,660
* SALARY: 340,000
* FASTER_PAYMENT: 219,656

Semua transaksi pada profiling awal memiliki status `COMPLETED` dan currency `GBP`.

---

### Account Balance History

Total records: **607,584**

* Unique account: 25,316
* Setiap account memiliki 24 records
* Periode: Januari 2023 sampai Desember 2024
* Opening balance minimum: -1,235,078.37
* Opening balance maximum: 918,906.17
* Closing balance minimum: -1,235,078.37
* Closing balance maximum: 918,906.17

Negative balance ditemukan pada data dan akan diperiksa lebih lanjut pada tahap **Data Quality** sebelum digunakan sebagai dasar analisis.

---

## 6. Key Data Characteristics

Beberapa karakteristik penting yang ditemukan:

1. `transaction` merupakan tabel dengan volume terbesar dan menjadi fact utama untuk analisis aktivitas transaksi.
2. `customer`, `account`, dan `product` berfungsi sebagai tabel master/dimension yang memberikan konteks terhadap transaksi.
3. Setiap customer memiliki minimal satu account.
4. Customer dapat memiliki beberapa account sehingga penggabungan customer dan transaction dapat menghasilkan banyak baris untuk customer yang sama.
5. `channel`, `transaction_type`, `direction`, dan `amount` memiliki variasi yang cukup untuk analisis bisnis.
6. `status` dan `currency` pada transaction tidak memiliki variasi pada dataset yang digunakan, sehingga belum menjadi fokus analisis.
7. Beberapa pola seperti seluruh transaksi credit yang berjumlah sama dengan transaksi salary dan seluruh transaksi salary yang recurring merupakan karakteristik dataset sintetis dan tidak boleh langsung dianggap sebagai pola perilaku nasabah dunia nyata.
8. `account_balance_history` dapat digunakan untuk melihat perubahan saldo dari waktu ke waktu.
9. Beberapa kolom mengandung informasi sensitif/PII seperti nama, email, nomor telepon, dan account number sehingga tidak diperlukan untuk dashboard analitik.

---

## 7. Data Understanding Conclusion

Dataset yang digunakan memiliki struktur relasional yang sesuai dengan kebutuhan proyek:

```text
Customer
   ↓
Account
   ↓
Transaction
   ↘
    Product

Account
   ↓
Balance History
```

Core dataset sudah berhasil diverifikasi dari sisi:

* struktur tabel
* grain
* primary key
* foreign key
* relationship
* jumlah data
* distribusi kategori
* periode waktu
* nilai transaksi
* karakteristik saldo

Tahap berikutnya adalah **Milestone 3 — Data Storage & Data Quality**, yang akan berfokus pada PostgreSQL, desain database, loading data, serta pemeriksaan kualitas data secara lebih mendalam.

---

## 8. Checklist

* [x] Menentukan sumber dataset
* [x] Generate dataset secara lokal
* [x] Memahami struktur core tables
* [x] Menentukan grain setiap tabel
* [x] Mengidentifikasi primary key
* [x] Mengidentifikasi foreign key
* [x] Memahami relationship antar tabel
* [x] Melakukan initial profiling
* [x] Melakukan primary key check
* [x] Melakukan relationship integrity check
* [x] Memahami karakteristik customer
* [x] Memahami karakteristik account
* [x] Memahami karakteristik transaction
* [x] Memahami karakteristik balance history
* [x] Menentukan core dataset untuk analisis
* [ ] Melakukan data quality check lebih mendalam

---

## 9. Milestone Output

Output Milestone 2:

* Dataset Banking Digital Twin hasil generate
* Core dataset teridentifikasi
* Data dictionary dipahami
* Grain dan relationship terdokumentasi
* Initial profiling selesai
* Primary key dan referential integrity tervalidasi
* Kandidat dimension dan fact teridentifikasi
* Data siap masuk ke tahap Data Storage & Data Quality
