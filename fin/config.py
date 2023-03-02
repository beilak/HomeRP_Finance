from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user = "fin_test_user"
    db_pwd = "fin_test_pwd"
    db_host = "127.0.0.1"
    db_port = "5431"
    db_name = "fin_test"
