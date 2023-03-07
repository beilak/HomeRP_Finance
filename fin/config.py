from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user = "fin_test_user"
    db_pwd = "fin_test_pwd"
    db_host = "127.0.0.1"
    db_port = "5000"
    db_name = "fin_test"

    auth_url = "http://127.0.0.1:8090"
    realm_name = "HomeRP"
    client_id = "HomeRP_Finance"
    token_leeway = 30
