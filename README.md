# 📄 Invoice Automation System

An end-to-end Python-based invoice automation pipeline that extracts invoice information from PDF documents, validates the extracted data, detects duplicate invoices, stores structured data in PostgreSQL, and generates CSV/Excel reports.

The system supports both digital/text-based PDFs and scanned/image-based PDFs through OCR.

---

## 🚀 Features

- 📄 PDF invoice processing
- 🔍 Automatic detection of digital/text PDFs
- 🧠 OCR support using Tesseract for scanned PDFs
- 📝 Automatic extraction of invoice fields
- 📦 Line-item extraction
- 🧮 Subtotal, tax, and total validation
- 🔁 Duplicate invoice detection
- 🗄️ PostgreSQL database integration
- 📊 Batch invoice processing
- 📁 Automatic file organization
- 📈 CSV report generation
- 📊 Excel report generation
- ⚠️ Manual-review workflow for invalid invoices
- 🐍 Built entirely with Python

---

## 🏗️ System Architecture

```text
                    Invoice PDF
                         │
                         ▼
                 File Validation
                         │
                         ▼
              Detect PDF Type
                  /          \
                 /            \
        Digital PDF          Scanned PDF
             │                    │
             ▼                    ▼
          PyMuPDF              Tesseract
             │                    │
             └──────────┬─────────┘
                        ▼
                  Extracted Text
                        │
                        ▼
                 Invoice Parser
                        │
                        ▼
                   Validation
                        │
              ┌─────────┴─────────┐
              │                   │
           Valid                Invalid
              │                   │
              ▼                   ▼
       Duplicate Check          Review
              │
       ┌──────┴──────┐
       │             │
     New           Duplicate
       │             │
       ▼             ▼
   PostgreSQL     PostgreSQL
       │
       ▼
 CSV / Excel Reports
```

---

## 📂 Project Structure

```text
invoice-automation/
│
├── app/
│   ├── extraction/
│   │   └── pdf_extractor.py
│   │
│   ├── ocr/
│   │   └── ocr_engine.py
│   │
│   ├── parser/
│   │   └── invoice_parser.py
│   │
│   ├── validation/
│   │   └── invoice_validator.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── invoice_repository.py
│   │
│   ├── reporting/
│   │   ├── invoice_report.py
│   │   └── export_report.py
│   │
│   └── pipeline.py
│
├── data/
│   ├── incoming/
│   ├── processed/
│   ├── review/
│   ├── failed/
│   └── reports/
│
├── main.py
├── automate.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application and automation |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | OCR for scanned invoices |
| Pillow | Image processing |
| OpenCV | OCR image preprocessing |
| NumPy | Image processing support |
| PostgreSQL | Persistent invoice database |
| Psycopg | PostgreSQL connectivity |
| Pandas | Report generation |
| OpenPyXL | Excel file generation |
| CSV | Lightweight report output |
| Linux | Development environment |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/DhruvThatte/invoice-automation.git
cd invoice-automation
```
## 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Tesseract OCR

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install tesseract-ocr
```

Verify:

```bash
tesseract --version
```

---

# 🐘 PostgreSQL Setup

The project uses PostgreSQL as its persistent database.

Create the database:

```sql
CREATE DATABASE invoice_db;
```

Create the application user:

```sql
CREATE USER invoice_app WITH PASSWORD 'YOUR_PASSWORD';
```

Grant the required permissions:

```sql
GRANT ALL PRIVILEGES ON DATABASE invoice_db TO invoice_app;
```

Connect to the database:

```bash
psql -U invoice_app -d invoice_db -h localhost
```

The exact PostgreSQL permissions may vary depending on your PostgreSQL installation.

---

# 🔐 Environment Configuration

Create your local `.env` file:

```bash
cp .env.example .env
```

Edit it:

```bash
nano .env
```

Example:

```env
DATABASE_URL=postgresql+psycopg2://invoice_app:YOUR_PASSWORD@localhost:5432/invoice_db

DB_HOST=localhost
DB_PORT=5432
DB_NAME=invoice_db
DB_USER=invoice_app
DB_PASSWORD=YOUR_PASSWORD
```

Never commit `.env` to GitHub.

---

# 🗄️ Initialize the Database

Run the database schema:

```bash
python -m app.database.schema
```

This creates the required PostgreSQL tables.

The database stores:

- Invoice information
- Vendor
- Invoice number
- Invoice date
- GSTIN
- Subtotal
- Tax
- Total
- Invoice line items

---

# ▶️ Process a Single Invoice

You can process an individual PDF using:

```bash
python main.py path/to/invoice.pdf
```

Example:

```bash
python main.py data/incoming/invoice.pdf
```

The pipeline performs:

```text
PDF
 ↓
Extraction / OCR
 ↓
Parsing
 ↓
Validation
 ↓
Duplicate Check
 ↓
PostgreSQL
```

---

# ⚡ Batch Automation

The main automation interface is:

```bash
python automate.py data/incoming/
```

Place invoice files inside:

```text
data/incoming/
```

For example:

```text
data/incoming/
├── invoice_001.pdf
├── invoice_002.pdf
├── invoice_003.pdf
└── invoice_004.pdf
```

Then run:

```bash
python automate.py data/incoming/
```

The system automatically processes every supported invoice.

Supported formats:

```text
.pdf
.jpg
.jpeg
.png
```

PDF processing uses the existing PDF pipeline, while scanned PDFs can be routed through OCR.

---

# 📁 Automatic File Organization

After processing, files are organized according to their result:

```text
data/
├── incoming/
│
├── processed/
│   └── successfully handled invoices
│
├── review/
│   └── invoices requiring manual review
│
├── failed/
│   └── invoices that could not be processed
│
└── reports/
    ├── invoice_report.csv
    └── invoice_report.xlsx
```

---

# 📊 Reports

After batch processing, the system generates:

```text
data/reports/invoice_report.csv
data/reports/invoice_report.xlsx
```

The reports contain fields such as:

| Field | Description |
|---|---|
| File Name | Source invoice file |
| Invoice Number | Extracted invoice number |
| Vendor | Seller/vendor |
| Invoice Date | Invoice date |
| GSTIN | GST identification number |
| Items | Number of line items |
| Subtotal | Invoice subtotal |
| Tax | Tax amount |
| Total | Final invoice amount |
| Status | Processing result |

Possible statuses include:

```text
approved
duplicate
review
failed
```

---

# 🧪 Validation

The system performs multiple validation checks before storing invoices.

### Required-field validation

Checks important fields such as:

```text
Vendor
Invoice Number
Invoice Date
Subtotal
Total
```

### Line-item validation

The system verifies that:

```text
Sum of line-item amounts ≈ Invoice subtotal
```

### Tax validation

The system verifies:

```text
Subtotal + Tax ≈ Total
```

### Duplicate detection

Invoices are checked against existing PostgreSQL records using the vendor and invoice number.

This prevents the same invoice from being inserted repeatedly.

---

# 🗃️ Database Design

The project uses a relational PostgreSQL design.

```text
invoices
   │
   │ 1
   │
   │
   │ many
   ▼
invoice_items
```

An invoice can contain multiple line items.

Example:

```text
Invoice
  INV-1001
      │
      ├── Laptop
      ├── Wireless Mouse
      └── Keyboard
```

This separates invoice-level information from line-item information and makes the data easier to query and analyze.

---

# 📈 Database Reporting

The project also includes database-level reporting.

Run:

```bash
python -m app.reporting.run_report
```

This provides:

- Total invoice count
- Total subtotal
- Total tax
- Total invoice value
- Average invoice value
- Vendor-level statistics
- Yearly invoice statistics

---

# 🔄 Complete Workflow

The complete workflow is:

```text
1. Place invoices in data/incoming/
                    ↓
2. Run automate.py
                    ↓
3. Detect invoice type
                    ↓
4. Extract PDF text
       OR
   Perform OCR
                    ↓
5. Parse invoice information
                    ↓
6. Extract line items
                    ↓
7. Validate invoice
                    ↓
8. Check for duplicates
                    ↓
9. Store valid invoice in PostgreSQL
                    ↓
10. Move source file
                    ↓
11. Generate CSV report
                    ↓
12. Generate Excel report
```

---

# 🧑‍💻 Example

Input:

```text
data/incoming/
├── invoice_001.pdf
├── invoice_002.pdf
├── invoice_003.pdf
└── invoice_004.pdf
```

Run:

```bash
python automate.py data/incoming/
```

Example result:

```text
============================================================
BATCH SUMMARY
============================================================
Files scanned:       4
New invoices:        2
Already processed:   1
Review required:     1
Failed:              0
============================================================

Generating reports...

CSV report:   data/reports/invoice_report.csv
Excel report: data/reports/invoice_report.xlsx
```

---

# 🎯 Project Goals

This project demonstrates practical implementation of:

- Python automation
- Document processing
- PDF extraction
- OCR
- Regular-expression/data parsing
- Data validation
- PostgreSQL database design
- Batch processing
- Duplicate detection
- Exception handling
- CSV/Excel reporting

The primary goal is to automate repetitive invoice-processing tasks while maintaining a structured and queryable database.

---

# 👨‍💻 Author

**Dhruv**

IoT undergrad interested in:

- Python
- Automation
- Machine Learning
- IoT
- Backend Development
- Database Systems

---

## ⭐ If you find this project useful

Feel free to fork the repository, experiment with the pipeline, and extend it with additional invoice formats or automation features.
