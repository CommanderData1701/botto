import unittest

from ..message_handlers import (
    Done,
    SetupHandler
)


class TestInitialSetupHandler(unittest.TestCase):

    def test_initial_setup_without_name_change(self):
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Hello")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("John")

        self.assertEqual(response, "Hello, John! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("John, Jane, Doe")
        expected_response = """Are John, Jane, Doe your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(response, "All set!")
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "John", "roommates": ["John", "Jane", "Doe"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_name_change(self):
        pass

    def test_initial_setup_with_user_change(self):
        pass

    def test_initial_setup_with_user_and_name_change(self):
        pass

    def test_initial_setup_with_invalid_response_at_name_change(self):
        pass

    def test_initial_setup_with_invalid_response_at_user_change(self):
        pass


if __name__ == '__main__':
    unittest.main()
