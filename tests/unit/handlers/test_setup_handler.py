import unittest

from botto.message_handlers import (
    Done,
    SetupHandler
)


class TestInitialSetupHandler(unittest.TestCase):

    def test_initial_setup_trivial(self):
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

        response = handler.generate_response("Jane, Doe")
        expected_response = """Are Jane, Doe your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "John", "roommates": ["Jane", "Doe"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_name_change(self):
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Nothing in life is to be feared; it is only to be understood.")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Max")

        self.assertEqual(response, "Hello, Max! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("no")
        self.assertEqual(response, "Ok, what is it then?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Marie")
        self.assertEqual(response, "Hello, Marie! Is this correct? (yes/no)")

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Albert, Nils, Werner")
        expected_response = """Are Albert, Nils, Werner your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "Marie", "roommates": ["Albert", "Nils", "Werner"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_user_change(self):
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Kann ich dir unsere Karte geben?")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Justus Jonas")

        self.assertEqual(response, "Hello, Justus Jonas! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Peter Shaw")
        expected_response = """Are Peter Shaw your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("no")
        self.assertEqual(response, "Ok, who are they then?")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Peter Shaw, Bob Andrews")
        expected_response = """Are Peter Shaw, Bob Andrews your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "Justus Jonas", "roommates": ["Peter Shaw", "Bob Andrews"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_user_and_name_change(self):
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Never tell me the odds!")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Indiana Jones")

        self.assertEqual(response, "Hello, Indiana Jones! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("no")
        self.assertEqual(response, "Ok, what is it then?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Han")
        self.assertEqual(response, "Hello, Han! Is this correct? (yes/no)")

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("C3PO, R2D2")
        expected_response = """Are C3PO, R2D2 your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("no")
        self.assertEqual(response, "Ok, who are they then?")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Luke, Leia, Chewbacca")
        expected_response = """Are Luke, Leia, Chewbacca your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "Han", "roommates": ["Luke", "Leia", "Chewbacca"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_invalid_response_at_name_change(self):
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Energize!")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Jean-Luc")

        self.assertEqual(response, "Hello, Jean-Luc! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("ys")
        self.assertEqual(response, "Answer must be 'yes' or 'no'")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Geordi, Beverly, Deanna, Worf, Data, Tasha")
        expected_response = """Are Geordi, Beverly, Deanna, Worf, Data, Tasha your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "Jean-Luc", "roommates": ["Geordi", "Beverly", "Deanna", "Worf", "Data", "Tasha"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_invalid_response_at_user_change(self):
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Energize!")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Jean-Luc")

        self.assertEqual(response, "Hello, Jean-Luc! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Geordi, Beverly, Deanna, Worf, Data, Tasha")
        expected_response = """Are Geordi, Beverly, Deanna, Worf, Data, Tasha your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)
        
        response = handler.generate_response("ys")
        self.assertEqual(response, "Answer must be 'yes' or 'no'")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "Jean-Luc", "roommates": ["Geordi", "Beverly", "Deanna", "Worf", "Data", "Tasha"]}
        self.assertEqual(handler(), result_dict)

    def test_initial_setup_with_duplicate_in_users(self) -> None:
        handler = SetupHandler()
        self.assertEqual(handler.state, SetupHandler.State.BEGIN)

        response = handler.generate_response("Energize!")

        self.assertEqual(response, "Hello! You are now the root user. What's your name?")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_NAME)

        response = handler.generate_response("Jean-Luc")

        self.assertEqual(response, "Hello, Jean-Luc! Is this correct? (yes/no)")
        self.assertEqual(handler.state, SetupHandler.State.CHANGE_NAME)

        response = handler.generate_response("yes")
        self.assertEqual(response, "Great! Now tell us who your roommates are. (Seperated by commas)")
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Jean-Luc, Beverly, Deanna, Worf, Data, Tasha")
        expected_response = "There are douplicates in the users. Please provide a unique list of users."
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.SET_UP_USERS)

        response = handler.generate_response("Geordi, Beverly, Deanna, Worf, Data, Tasha")
        expected_response = """Are Geordi, Beverly, Deanna, Worf, Data, Tasha your roommates? (yes/no)"""
        self.assertEqual(response, expected_response)
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)
        
        response = handler.generate_response("ys")
        self.assertEqual(response, "Answer must be 'yes' or 'no'")
        self.assertEqual(handler.state, SetupHandler.State.CONFIRM_USERS)

        response = handler.generate_response("yes")
        self.assertEqual(handler.state, Done.DONE)
        self.assertEqual(response, "All set!")
        result_dict = {"root_name": "Jean-Luc", "roommates": ["Geordi", "Beverly", "Deanna", "Worf", "Data", "Tasha"]}
        self.assertEqual(handler(), result_dict)


if __name__ == '__main__':
    unittest.main()
