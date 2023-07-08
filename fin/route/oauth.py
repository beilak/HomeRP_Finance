"""oAuth for route"""
import json
import os
from typing import Final
from fastapi import Header
from fastapi.security import OAuth2
from fastapi.openapi.models import (
    OAuthFlowAuthorizationCode,
    OAuthFlows as OAuthFlowModel
)
from fastapi import Security, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from fin.containers import FinContainer
from fin.adapters.auth.keycloak_adapter import KeycloakAdapter
from fin.models.common import UserProfile


OAUTH_FLOWS: Final[OAuth2] = OAuth2(
    flows=OAuthFlowModel(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl=os.getenv(
                "AUTHORIZATION_URL",
                "http://127.0.0.1:8090/realms/HomeRP/protocol/openid-connect/auth"
            ),
            tokenUrl=os.getenv(
                "TOKEN_URL",
                "http://127.0.0.1:8090/realms/HomeRP/protocol/openid-connect/token"
            )
        )
    )
)


@inject
async def oauth_check(
        x_token: str = Header()
        # token: str = Security(OAUTH_FLOWS),
        # keycloak_adapter: KeycloakAdapter = Depends(Provide[FinContainer.keycloak_adapter])
) -> UserProfile:
    """Auth check and return User Login"""
    # ToDo TMP Auth use X-Token (as a dict). Must be be JWT
    token_json = json.loads(x_token)
    return UserProfile(
        login=token_json['login'],
        unit_id=token_json['unit_id'],
    )
    # try:
    #     decoded_token = await keycloak_adapter.check_token(token.split()[1])
    # except Exception:
    #     raise HTTPException(status_code=400, detail="Token header invalid")
    # return decoded_token["email"]
