from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_pwd: str
    db_host: str
    db_port: int
    db_name: str

    #ToDo add Auth
    # auth_url = "http://127.0.0.1:8090"
    # realm_name = "HomeRP"
    # client_id = "HomeRP_Finance"
    # token_leeway = 30

    mq_host: str
    mq_user: str
    mq_pass: str
    mq_listen_queue: str
