import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "no-secret"),
    DATABASE_URL=(str, "postgres://username:password@localhost:port/database_name"),
)
