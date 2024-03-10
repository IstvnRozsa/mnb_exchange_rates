import psycopg2
import json

# Define your PostgreSQL connection parameters
DB_NAME = "dyntell_api_saver_db"
DB_USER = "postgres"
DB_PASSWORD = "Brie10"
DB_HOST = "localhost"
DB_PORT = "5435"


with open("data/exchange_rates.json", "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)
  


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor object
cur = conn.cursor()

# Define the SQL query to create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS exchange_rates_mnb (
    id SERIAL PRIMARY KEY,
    deviza_id VARCHAR(255),
    description VARCHAR(255),
    rate NUMERIC,
    date DATE
);
'''

# Execute the create table query
cur.execute(create_table_query)


# Iterate over the JSON data and insert it into the database if the date doesn't already exist
for item in json_data:
    deviza_id = item['deviza_id']
    description = item['description']
    rate = item['rate'].replace(",", ".")
    date = item['date']

    # Construct the SQL query
    sql = "INSERT INTO exchange_rates_mnb (deviza_id, description, rate, date) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM exchange_rates_mnb WHERE date = %s AND deviza_id = %s)"
    # Execute the SQL query
    cur.execute(sql, (deviza_id, description, rate, date, date, deviza_id))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
