"""Keycloak Adapter"""
from keycloak import KeycloakOpenID
#from cryptography.hazmat.primitives import serialization


class KeycloakAdapter:
    def __init__(
            self,
            auth_url: str,
            realm_name: str,
            client_id: str,
            leeway: int
    ) -> None:
        self._open_id = KeycloakOpenID(
            server_url=auth_url,
            client_id=client_id,
            realm_name=realm_name,
            verify=True,
        )
        # key_der_base64 = self._open_id.certs()
        # print(".......", key_der_base64)
        # key_der = b64decode(key_der_base64.encode())
        # public_key = serialization.load_der_public_key()
        # serialization.

        # self._jwks = f"""-----BEGIN PUBLIC KEY-----{self._open_id.public_key()}-----END PUBLIC KEY-----"""
        self._jwks = f"-----BEGIN PUBLIC KEY-----\n{self._open_id.public_key()}\n-----END PUBLIC KEY-----"

        # print(self._jwks)
        self._check_token_opt = {
            "verify_signature": True,
            "verify_aud": False,
            "exp": True,
            "leeway": leeway
        }

    async def check_token(self, client_token: str) -> dict:
        """Check token and return decoded token"""
        return self._open_id.decode_token(
            client_token,
            key=self._jwks,
            options=self._check_token_opt
        )
