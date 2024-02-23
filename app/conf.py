class Settings:
    DATABASE_URL: str
    ECHO: bool


settings = Settings()

settings.DATABASE_URL = "postgresql+psycopg://mk_burger_fast_user:mk_burger_fast_password@localhost:5432/mk_burger_fast"
settings.ECHO = False
