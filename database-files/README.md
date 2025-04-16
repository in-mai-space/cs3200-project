# Mock Data Generation Script

This script generates and inserts mock data into the Uplift database. It uses the Faker library to create realistic data for all tables in the database schema.

## Prerequisites

1. Python 3.x installed
2. Docker and Docker Compose installed
3. Required Python packages

## Setup

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install faker mysql-connector-python python-dotenv
```

3. Create a `.env` file in your project's root directory with the following content:
```
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=uplift
MYSQL_ROOT_PASSWORD=password
```

## Running with Docker

1. Start your Docker containers:
```bash
task all:up
```

2. Wait for the MySQL container to be fully initialized (about 30 seconds)

3. Run the mock data generation script:
```bash
python database-files/generate_and_insert_mock_data.py
```

The script will:
- Connect to your MySQL database running in Docker
- Generate mock data for all tables
- Insert the data while maintaining referential integrity
- Print progress messages for each table
- Handle duplicate entries gracefully

## Data Generation Details

The script generates the following quantities of data:
- Users: 100
- Organizations: 20
- Programs: 50
- Categories: 10
- Applications: 200
- Feedback Forms: 150
- Locations: 100

## Troubleshooting

If you encounter any errors:

1. **Connection Error**: 
   - Verify Docker containers are running (`task all:up`)
   - Check your `.env` file settings
   - Ensure MySQL container is fully initialized (wait 30 seconds after starting)

2. **Duplicate Entry Errors**:
   - The script handles duplicates automatically
   - If you want to start fresh, you can:
     ```bash
     task db:reset  # This will recreate the database
     python database-files/generate_and_insert_mock_data.py
     ```

3. **Permission Errors**:
   - Ensure your MySQL user has the necessary permissions
   - Check if the database exists and is accessible

## Notes

- The script maintains referential integrity by inserting data in the correct order
- It checks for existing entries to prevent duplicates
- All generated data is realistic and follows the database schema constraints
- Progress messages will show you how many records were inserted for each table
- The `database-files` directory is created automatically when you clone the repository

```
venv 