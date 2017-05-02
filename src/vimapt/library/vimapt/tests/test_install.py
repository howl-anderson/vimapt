import unittest

from vimapt.Install import Install


class TestInstall(unittest.TestCase):
    def test_main(self):
        install = Install("./vim")
        install.install_package("./vimapt_1.0-1.vpb")

    def test_underline_parse_requirement(self):
        def parse_string_valid():
            requirement_data = "valid-package"
            got_result = Install(None)._parse_requirement(requirement_data)
            expected_result = None

            self.assertEqual(got_result, expected_result)

        parse_string_valid()

        def parse_string_invalid():
            requirement_data = "invalid-package"
            got_result = Install(None)._parse_requirement(requirement_data)
            expected_result = None

            self.assertEqual(got_result, expected_result)

        parse_string_invalid()

        def parse_list_valid():
            requirement_data = [
                "valid-package-one",
                "valid-package-two"
            ]
            got_result = Install(None)._parse_requirement(requirement_data)
            expected_result = None

            self.assertEqual(got_result, expected_result)

        parse_list_valid()

        def parse_list_invalid():
            requirement_data = [
                "invalid-package-one",
                "invalid-package-two"
            ]
            got_result = Install(None)._parse_requirement(requirement_data)
            expected_result = None

            self.assertEqual(got_result, expected_result)

        parse_list_invalid()
