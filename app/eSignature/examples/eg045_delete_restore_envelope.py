from docusign_esign import FoldersApi, FoldersRequest

from ...docusign import create_api_client


class Eg045DeleteRestoreEnvelopeController:
    @staticmethod
    def move_envelope(args):
        #ds-snippet-start:eSign45Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        folders_api = FoldersApi(api_client)
        #ds-snippet-end:eSign45Step2

        #ds-snippet-start:eSign45Step3
        folders_request = FoldersRequest(
            envelope_ids=[args["envelope_id"]],
            
            # add from_folder_id parameter if its value is provided
            **({"from_folder_id": args["from_folder_id"]} if args.get("from_folder_id") else {})
        )
        #ds-snippet-end:eSign45Step3

        #ds-snippet-start:eSign45Step4
        results = folders_api.move_envelopes(account_id=args["account_id"], folder_id=args["folder_id"], folders_request=folders_request)
        #ds-snippet-end:eSign45Step4
        return results
