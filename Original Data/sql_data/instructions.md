
# MySQL Dataset Setup

This guide helps you import SQL dump files into a MySQL database.

## Prerequisites

- **MySQL**: Install from [here](https://dev.mysql.com/downloads/installer/).
- **Python** (optional): Install from [here](https://www.python.org/), then run:
  ```bash
  pip install mysql-connector-python pandas
  ```

## Instructions

### 1. Create the Database
Log into MySQL:
```bash
mysql -u root -p
```
Create the database:
```sql
CREATE DATABASE IF NOT EXISTS wildfire_data;
USE wildfire_data;
```

### 2. Import the `.sql` Files
Download the `.sql` files from the repository and import them:
```bash
mysql -u root -p wildfire_data < /path/to/daily_co.sql
```
Repeat for each file (`daily_co.sql`, `daily_no2.sql`, etc.).

### 3. Use the dataset
