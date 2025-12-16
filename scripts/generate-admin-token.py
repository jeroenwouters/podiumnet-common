import requests
import sys

admin_password = "admin"
admin_token_lifespan = 126144000
admin_username = "admin"
client_id = "podiumnet-dashboard-elody"
client_secret = "3ba1d936-67bb-c3b7-1a37-016d528caa0c"
keycloak_url = "http://keycloak.localhost:8000"


def create_admin_user():
    json = {
        "username": admin_username,
        "enabled": "true",
    }

    requests.post(
        f"{keycloak_url}/auth/admin/realms/podiumnet/users", headers=headers, json=json
    )


def delete_admin_user():
    requests.delete(
        f"{keycloak_url}/auth/admin/realms/podiumnet/users/{admin_user_id}",
        headers=headers,
    )


def get_admin_access_token():
    data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": admin_username,
        "password": admin_password,
    }

    return requests.post(
        f"{keycloak_url}/auth/realms/master/protocol/openid-connect/token", data=data
    ).json()["access_token"]


def get_admin_user_id():
    return requests.get(
        f"{keycloak_url}/auth/admin/realms/podiumnet/users?username={admin_username}",
        headers=headers,
    ).json()[0]["id"]


def get_public_key():
    keys = requests.get(
        f"{keycloak_url}/auth/admin/realms/podiumnet/keys",
        headers=headers,
        json=realm_config,
    ).json()["keys"]
    for key in keys:
        if "publicKey" in key:
            return key["publicKey"]
    return None


def get_realm_config():
    return requests.get(
        f"{keycloak_url}/auth/admin/realms/podiumnet", headers=headers
    ).json()


def get_user_token():
    try:
        username = sys.argv[1]
    except:
        username = None

    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username or admin_username,
        "password": username or admin_password,
    }

    return requests.post(
        f"{keycloak_url}/auth/realms/podiumnet/protocol/openid-connect/token", data=data
    ).json()["access_token"]


def update_admin_user_password():
    json = {
        "type": admin_password,
        "temporary": "false",
        "value": admin_username,
    }

    requests.put(
        f"{keycloak_url}/auth/admin/realms/podiumnet/users/{admin_user_id}/reset-password",
        headers=headers,
        json=json,
    )


def update_realm():
    requests.put(
        f"{keycloak_url}/auth/admin/realms/podiumnet", headers=headers, json=realm_config
    )


if __name__ == "__main__":
    headers = {"Authorization": f"Bearer {get_admin_access_token()}"}
    realm_config = get_realm_config()
    original_access_token_lifespan = realm_config["accessTokenLifespan"]
    original_sso_session_max_lifespan = realm_config["ssoSessionMaxLifespan"]
    realm_config["accessTokenLifespan"] = admin_token_lifespan
    realm_config["ssoSessionMaxLifespan"] = admin_token_lifespan
    update_realm()
    create_admin_user()
    admin_user_id = get_admin_user_id()
    update_admin_user_password()
    print(f'STATIC_JWT="{get_user_token()}"')
    print(f'STATIC_PUBLIC_KEY="{get_public_key()}"')
    print(f'STATIC_ISSUER="{keycloak_url}/auth/realms/podiumnet"')
    realm_config["accessTokenLifespan"] = original_access_token_lifespan
    realm_config["ssoSessionMaxLifespan"] = original_sso_session_max_lifespan
    update_realm()
    delete_admin_user()