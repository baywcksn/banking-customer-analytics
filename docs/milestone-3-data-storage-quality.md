# Milestone 3 — Data Storage & Data Quality

## 1. Tujuan

Milestone ini bertujuan untuk membangun penyimpanan data menggunakan PostgreSQL serta memastikan data yang telah dimuat memiliki struktur, integritas, kelengkapan, dan nilai yang sesuai untuk tahap analisis berikutnya.

---

## 2. Database Setup

Database PostgreSQL dijalankan menggunakan Docker.

Konfigurasi utama:

* Database: `banking_analytics`
* User: `banking_user`
* PostgreSQL: 16
* Host port: `5434`
* Container: `banking-analytics-postgres`

Database digunakan sebagai centralized data storage sebelum data ditransformasi menggunakan dbt pada milestone berikutnya.

---

## 3. Struktur Tabel

Lima tabel utama dibuat di PostgreSQL:

| Tabel                     | Jumlah Baris | Primary Key      |
| ------------------------- | -----------: | ---------------- |
| `customer`                |       10.000 | `customer_id`    |
| `product`                 |           86 | `product_id`     |
| `account`                 |       25.316 | `account_id`     |
| `transaction`             |    7.610.818 | `transaction_id` |
| `account_balance_history` |      607.584 | `history_id`     |

Relasi utama antar tabel:

```text
customer
   │
   │ 1:N
   ▼
account
   ├── N:1 → product
   │
   ├── 1:N → transaction
   │
   └── 1:N → account_balance_history
```

---

## 4. Data Loading

Data dari dataset Banking Digital Twin dimuat ke PostgreSQL menggunakan Python dan Pandas.

Untuk tabel transaksi yang berukuran besar, proses loading dilakukan menggunakan pendekatan chunking dengan ukuran 50.000 baris per batch agar penggunaan memory lebih terkontrol.

Data yang berhasil dimuat:

* 10.000 customer
* 86 product
* 25.316 account
* 7.610.818 transaction
* 607.584 account balance history

---

## 5. Data Quality Checks

### 5.1 Row Count dan Primary Key Uniqueness

Setiap tabel diperiksa berdasarkan jumlah baris dan jumlah ID unik.

Hasil:

| Tabel                     | Row Count | Unique ID | Status |
| ------------------------- | --------: | --------: | ------ |
| `customer`                |    10.000 |    10.000 | Lolos  |
| `product`                 |        86 |        86 | Lolos  |
| `account`                 |    25.316 |    25.316 | Lolos  |
| `account_balance_history` |   607.584 |   607.584 | Lolos  |
| `transaction`             | 7.610.818 | 7.610.818 | Lolos  |

Tidak ditemukan duplicate primary key pada tabel yang diperiksa.

---

### 5.2 Foreign Key Integrity

Integritas hubungan antar tabel diperiksa menggunakan pengecekan orphan records.

Hasil:

| Relasi                              | Orphan Records | Status |
| ----------------------------------- | -------------: | ------ |
| `transaction → account`             |              0 | Lolos  |
| `account → customer`                |              0 | Lolos  |
| `account_balance_history → account` |              0 | Lolos  |

Tidak ditemukan record yang memiliki foreign key tetapi tidak memiliki parent record.

---

### 5.3 Missing Values pada Transaction

Kolom merchant diperiksa karena tidak semua jenis transaksi berhubungan dengan merchant.

Hasil:

* Total transaksi: 7.610.818
* `merchant_id` terisi: 6.685.502
* `merchant_name` terisi: 7.025.502
* `mcc_code` terisi: 6.685.502

Missing value pada informasi merchant tidak langsung dianggap sebagai error.

Pengecekan berdasarkan `transaction_type` menunjukkan bahwa:

* `CONTACTLESS` dan `PURCHASE` memiliki informasi merchant.
* `ATM_WITHDRAWAL`, `SALARY`, dan `FASTER_PAYMENT` tidak memiliki `merchant_id`.

Dengan demikian, missing value pada kolom merchant bersifat kontekstual dan sesuai dengan karakteristik jenis transaksi.

---

### 5.4 Kelengkapan Field Utama

Kolom utama pada tabel `transaction` diperiksa untuk memastikan tidak terdapat nilai NULL.

Kolom yang diperiksa:

* `account_id`
* `amount`
* `direction`
* `transaction_date`
* `transaction_timestamp`
* `status`

Seluruh kolom memiliki jumlah nilai terisi sebanyak 7.610.818 baris.

Status: **Lolos**.

---

### 5.5 Validasi Nilai Transaksi

Nilai transaksi diperiksa menggunakan nilai minimum, maksimum, dan jumlah nilai yang kurang dari atau sama dengan nol.

Hasil:

* Minimum amount: `0.32`
* Maximum amount: `28,521.51`
* Invalid amount (`<= 0`): `0`

Seluruh nilai transaksi memiliki nilai positif.

Status: **Lolos**.

---

### 5.6 Validasi Direction

Distribusi `direction` diperiksa untuk memastikan kategori transaksi sesuai dengan struktur dataset.

Hasil:

| Direction |    Jumlah |
| --------- | --------: |
| `DEBIT`   | 7.270.818 |
| `CREDIT`  |   340.000 |

Tidak ditemukan kategori direction lain.

Status: **Lolos**.

---

### 5.7 Validasi Status

Distribusi status transaksi diperiksa.

Hasil:

| Status      |    Jumlah |
| ----------- | --------: |
| `COMPLETED` | 7.610.818 |

Seluruh transaksi memiliki status `COMPLETED`.

Status: **Lolos**.

---

### 5.8 Validasi Rentang Tanggal

Rentang tanggal transaksi diperiksa untuk memastikan tidak terdapat tanggal di luar periode dataset.

Hasil:

* Tanggal paling awal: `2023-01-01`
* Tanggal paling akhir: `2024-12-31`
* Tanggal di luar periode: `0`

Status: **Lolos**.

---

### 5.9 Konsistensi Transaction Date dan Timestamp

Tanggal pada `transaction_timestamp` dibandingkan dengan `transaction_date`.

Hasil:

* Jumlah timestamp yang tanggalnya tidak sesuai dengan `transaction_date`: `0`

Dengan demikian, kedua kolom tanggal tersebut konsisten.

Status: **Lolos**.

---

### 5.10 Transaction Coverage

Dari 25.316 account, sebanyak 13.955 account memiliki setidaknya satu transaksi selama periode pengamatan.

Hal ini bukan merupakan data quality error. Account tanpa transaksi tetap dapat merupakan record yang valid dan nantinya dapat digunakan untuk analisis customer/account activity.

---

## 6. Index Database

PostgreSQL secara otomatis membuat index untuk setiap primary key.

Index yang tersedia:

* `customer_pkey`
* `product_pkey`
* `account_pkey`
* `transaction_pkey`
* `account_balance_history_pkey`

Index tambahan pada foreign key belum dibuat pada tahap ini. Index tambahan akan dipertimbangkan berdasarkan pola query dan kebutuhan performa pada tahap analisis dan transformation.

---

## 7. Kesimpulan

Database PostgreSQL berhasil dibangun dan seluruh data utama berhasil dimuat.

Hasil data quality check menunjukkan:

* Primary key tidak memiliki duplicate.
* Tidak ditemukan orphan record pada foreign key.
* Field utama transaction tidak memiliki NULL.
* Missing value pada merchant dapat dijelaskan berdasarkan jenis transaksi.
* Seluruh nilai transaksi lebih besar dari nol.
* Direction memiliki kategori yang sesuai.
* Seluruh transaksi berstatus `COMPLETED`.
* Rentang tanggal transaksi sesuai dengan periode dataset.
* `transaction_date` konsisten dengan tanggal pada `transaction_timestamp`.

Dengan demikian, data telah siap digunakan untuk tahap berikutnya, yaitu **Data Transformation & Data Modeling menggunakan dbt**.