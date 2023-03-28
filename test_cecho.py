import unittest
from unittest.mock import MagicMock, patch
from cecho import CEcho

class TestCEcho(unittest.TestCase):
    

    def test_verify_association_established(self):
        with patch('cecho.AE') as mock_ae:
            # configure this mock_ae obj
            # return value: mock_assoc
            mock_ae.add_requested_context.return_value = None
            mock_ae.associate.return_value = MagicMock()
            mock_assoc = mock_ae.associate.return_value
            mock_assoc.send_c_echo.return_value = MagicMock(Status=0x0000)

            c_echo = CEcho('127.0.0.1', 4242)
            c_echo.ae = mock_ae
            c_echo.assoc = mock_assoc

            #mock_assoc.send_c_echo.assert_called_once()

            #if success
            self.assertTrue(c_echo.verify())
            mock_assoc.release.assert_called_once()

            # if failed
            mock_assoc.send_c_echo.return_value = None
            self.assertFalse(c_echo.verify())
            assert mock_assoc.release.call_count == 2

            # if connection not established
            mock_assoc.is_established = False
            self.assertFalse(c_echo.verify())
            assert mock_assoc.release.call_count == 2

            




if __name__ == '__main__':
    unittest.main()