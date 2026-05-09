DB_USERNAME = "postgres"
DB_PASSWORD = "8374Ram"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "task_manager"

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False