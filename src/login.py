from os import getenv
from msal import PublicClientApplication
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("msal").setLevel(logging.DEBUG)
logging.getLogger("msal.broker").setLevel(logging.DEBUG)


def login(tenant_id: str, client_id: str, scopes: list[str]):
    app = PublicClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        enable_broker_on_mac=True,
        enable_broker_on_windows=True,
    )

    return app.acquire_token_interactive(
        scopes,
        parent_window_handle=app.CONSOLE_WINDOW_HANDLE,
    )


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    result = login(
        tenant_id=getenv("AZURE_AD_TENANT_ID"),
        client_id=getenv("AZURE_AD_CLIENT_ID"),
        scopes=[getenv("AZURE_AD_SCOPES")],
    )

    print(result)
