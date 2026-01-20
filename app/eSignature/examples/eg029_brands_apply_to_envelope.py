import base64
from datetime import datetime as dt, timezone
from os import path
from docusign_esign import AccountsApi, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients
from docusign_esign.client.api_exception import ApiException
from flask import request, session
from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

class Eg029BrandsApplyToEnvelopeController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than the characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        brand_id = request.form.get("brand")

        args = {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "envelope_args": {
                "signer_name": signer_name,
                "signer_email": signer_email,
                "brand_id": brand_id
            }

        }
        return args

    @classmethod
    def worker(cls, args):
        """
        1. Create an API client
        2. Create an envelope definition object
        3. Apply the brand to the envelope using SDK
        """

        # Construct your API headers
        #ds-snippet-start:eSign29Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign29Step2

        # Construct your request body
        #ds-snippet-start:eSign29Step4
        envelope_api = EnvelopesApi(api_client)
        envelope_definition = cls.make_envelope(args["envelope_args"])

        # Call the eSignature REST API
        (response, status, headers) = envelope_api.create_envelope_with_http_info(account_id=args["account_id"], envelope_definition=envelope_definition)

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign29Step4

        return response

    #ds-snippet-start:eSign29Step3
    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        """

        # Open the example file
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        document = Document(
            document_base64=base64_file_content,
            name="lorem",
            file_extension="pdf",
            document_id=1
        )

        signer = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            recipient_id="1",
            routing_order="1"
        )

        sign_here = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="572",
            anchor_x_offset="75"
        )

        signer.tabs = Tabs(sign_here_tabs=[sign_here])

        envelope_definition = EnvelopeDefinition(
            email_subject="Please Sign",
            documents=[document],
            recipients=Recipients(signers=[signer]),
            status="sent",
            brand_id=args["brand_id"],
        )

        return envelope_definition
    #ds-snippet-end:eSign29Step3

    @staticmethod
    def get_brands(args):
        """Retrieve all brands using the AccountBrands::List"""

        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        try:
            account_api = AccountsApi(api_client)
            (response, status, headers) = account_api.list_brands_with_http_info(account_id=args["account_id"])

            remaining = headers.get("X-RateLimit-Remaining")
            reset = headers.get("X-RateLimit-Reset")

            if remaining is not None and reset is not None:
                reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
                print(f"API calls remaining: {remaining}")
                print(f"Next Reset: {reset_date}")

            return response.brands
        except ApiException as err:
            return process_error(err)