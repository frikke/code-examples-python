from datetime import datetime as dt, timezone
from docusign_rooms import (
    FormGroupsApi,
    FormGroupSummaryList,
    FormLibrariesApi,
    FormGroupFormToAssign,
)
from docusign_rooms import FormSummaryList
from flask import session, request

from app.rooms import create_rooms_api_client


class Eg009AssignFormToFormGroupController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "form_group_id": request.form.get("form_group_id"),
            "form_id": request.form.get("form_id")
        }

    @staticmethod
    def get_form_groups(args):
        """
        1. Create an API Client with headers
        2. GET Form Groups via FormGroupsAPI
        """

        # Create an API with headers with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # GET Form Groups via FormGroupsAPI

        #ds-snippet-start:Rooms9Step4
        form_groups_api = FormGroupsApi(api_client)
        (response, status, headers) = form_groups_api.get_form_groups_with_http_info(
            account_id=args["account_id"]
        )  # type: FormGroupSummaryList

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms9Step4

        return response.form_groups

    @staticmethod
    def get_forms(args):
        """
        1. Create an API client with headers
        2. Get first form library id
        3. Get forms
        """

        # Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        #ds-snippet-start:Rooms9Step3
        form_libraries_api = FormLibrariesApi(api_client)
        (form_libraries, status, headers) = form_libraries_api.get_form_libraries_with_http_info(
            account_id=args["account_id"]
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        first_form_library_id = form_libraries.forms_library_summaries[0].forms_library_id

        # Get forms
        (form_library_forms, status, headers) = form_libraries_api.get_form_library_forms_with_http_info(
            form_library_id=first_form_library_id, account_id=args["account_id"]
        )   # type: FormSummaryList

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms9Step3
        
        return form_library_forms.forms

    @staticmethod
    def worker(args):
        """
        1. Create an API Client with headers
        2. Create FormGroupFormToAssign Object
        3. Assign form to a form group via FormGroups API
        """

        # Create an API client with headers
        #ds-snippet-start:Rooms9Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms9Step2
        
        form_groups_api = FormGroupsApi(api_client)

        # Create FormGroupFormToAssign Object
        #ds-snippet-start:Rooms9Step5
        form_group_to_assign = FormGroupFormToAssign(
            form_id=args["form_id"], is_required=True
        )
        #ds-snippet-end:Rooms9Step5

        # Assign form to a form group via FormGroups API
        #ds-snippet-start:Rooms9Step6
        (response, status, headers) = form_groups_api.assign_form_group_form_with_http_info(
            form_group_id=args["form_group_id"], account_id=args["account_id"],
            body=form_group_to_assign
        )   # type: FormGroupFormToAssign

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms9Step6

        return response
