from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

username = "root"
password = "YourProject@2026"
host = "127.0.0.1"
port = 3306
database = "retail_logistics"

connection_url = URL.create(
    "mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))

        print("MySQL connection successful!")
        print("Connected database:", result.fetchone()[0])

except Exception as e:
    print("MySQL connection failed!")
    print("Error:", e)