# Finance Tracker

![Status](https://img.shields.io/badge/status-early%20development-yellow)
![Status](https://img.shields.io/badge/status-work%20in%20progress-orange)

> ⚠️ **Work in Progress**: This project is in early development and not production-ready.

A personal finance management application that syncs transaction data from Google Drive spreadsheets and provides insightful financial analytics through a web interface.

## Features

- 📊 Automatic transaction synchronization from Google Drive spreadsheets
- 📈 Category-based expense analysis
- ✈️ Travel expenses tracking
- 🌐 Clean Flask web interface for data visualization

## Prerequisites

- Docker
- Python 3.x
- Google Drive API credentials (for spreadsheet access)
- A Google Sheets document with your transaction data

## Installation

1. **Clone the repository**

  ```bash
  git clone <repository-url>
  cd <project-directory>
  ```

2. **Configure environment variables**
  Create a `.env` file in the root directory with your configuration. configuration. You can copy the `.env.example` file:

  ```bash
  cp .env.example .env
  ```

  The .env file looks like this:

  ```env
  # Google Drive Configuration
  GOOGLE_DRIVE_FILE_ID=your_google_file_id_here

  # Database Configuration
  DB_USER=finance_user
  DB_PASSWORD=your_secure_password_here
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=finance
  ```

  You need to replace your_google_file_id_here with the ID that matches your spreadsheet.

  This application use a PostgreSQL database by default. You can deploy a PostgreSQL instance using Docker like this:

  ```bash
  docker compose up -d
  ```

  Remember to update your database configuration accordingly.


## Usage

### 1. Start the Database

Launch the database using Docker Compose:

```bash
docker-compose up -d
```

### 2. Sync Transactions

Run the synchronization script to import data from your Google Drive spreadsheet:

```bash
python services/sync_transactions.py
```

This script will:

- Connect to your Google Drive spreadsheet
- Fetch all transaction data
- Store the data in the configured database

### 3. Start the Web Application

Launch the Flask web application:

```bash
python main.py
```

The application will be available at `http://localhost:5000`.
