import json
import unittest

from LogGroupToSlack import app


class context:
    def __init__(self):
        self.log_stream_name = "test_log_stream_name"
        self.log_group_name = "test_log_group_name"


class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.cwl_event = {
            "awslogs": {
                "data": "H4sIAAAAAAAAAEWQXW/bIBiF/4rF1aYW82nA7lWmpom2VJoUa7toogljlqASYwFZ11X97yPdpsEV5zkcDu8LONmU9MH2z7MFHbhd9Itv98vtdrFagmsQniYbiywx5YpS1VAsiuzDYRXDeS4EWZPQkx2Sy/YP2eZo9amgC5kObvqJGjmKYeRibFXD5dhow0ajB0mo1pgSVS6m85BMdHN2YbpzPtuYQPcANn9f6sPWa/MI19b78DVEP96dJ3Mx/1cgXa4/3babL6t1uwH7tzLLH3bKl6QX4MbSiXGFOW6VFII0lLdMKEIZY5JLggmTmBRGFVGMU0GVkKptWoJ5aZhdGVXWp/Jr0ggsRCsFbzG7/jfCEt/wmomaNLguCRUs+4EI9PE8IVqSOyw7SjvOqytc1r7agdWyr5CO2RlvEzIumQDTrOMjPD4P0Y3QaO+hCdNkTQ4RJpvPMyyGDGm17vvPiNRkByqKccWwkiUSluMO3IdfznuNmhpX70w4zTq7wdubanGM9nv6EDIqRW+qq2POc4eQfpPr4kQxDIW+3wHwun/9DU703OghAgAA"
            }
        }

    @unittest.skip("Non-asserting test for main function")
    def test_lambda_cwl_handler(self):
        # act
        app.lambda_handler(self.cwl_event, context())

    def test_event_decoder(self):
        # act
        result = app.event_decoder(self.cwl_event)

        # assert
        self.assertTrue("owner" in result)
