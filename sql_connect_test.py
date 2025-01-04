import pyodbc

server = 'DIST-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_SJames'
username = 'SJames'
password = 'ApbI766*'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Verify current database
    cursor.execute("SELECT DB_NAME()")
    current_db = cursor.fetchone()
    print(f"Connected to database: {current_db[0]}")

    # Verify current user
    cursor.execute("SELECT USER_NAME()")
    current_user = cursor.fetchone()
    print(f"Connected as user: {current_user[0]}")

    # Create table
    cursor.execute('''
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(50),
            age INT
        )
    ''')

    # Insert data
    users = [
        (1, 'User1', 30),
        (2, 'User2', 25),
        (3, 'User3', 35)
    ]
    cursor.executemany('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', users)

    # Commit the changes
    conn.commit()

    # Fetch data
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except pyodbc.Error as ex:
    print(f"An error occurred: {ex}")
finally:
    if 'conn' in locals():
        cursor.execute('DROP TABLE users')
        conn.close()