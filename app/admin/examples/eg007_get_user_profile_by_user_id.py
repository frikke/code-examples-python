from datetime import datetime as dt, timezone
from docusign_admin import ApiClient, UsersApi
from flask import session, request

from ...ds_config import DS_CONFIG
from app.admin.utils import get_organization_id

class Eg007GetUserProfileByUserIdController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id, # Represents your {ORGANIZATION_ID},
            "user_id": request.form.get("user_id"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get user profile data
        """

        access_token = args["access_token"]
        org_id = args["organization_id"]
        user_id = args["user_id"]

        # Create an API client with headers
        #ds-snippet-start:Admin7Step2
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-end:Admin7Step2

        #ds-snippet-start:Admin7Step3
        users_api = UsersApi(api_client=api_client)

        (results, status, headers) = users_api.get_user_ds_profile_with_http_info(
            organization_id=org_id,
            user_id=user_id)
        
        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Admin7Step3

        return results
