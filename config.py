from dotenv import load_dotenv
import os

load_dotenv()


# Db data
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST_NAME = os.getenv("DB_HOST_NAME")
DB_NAME = os.getenv("DB_NAME")

# secret key
SECRET_KEY = os.getenv("SECRET_KEY")