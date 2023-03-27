import unittest
from unittest.mock import MagicMock
from cecho import CEcho, Verification

class TestCEcho(unittest.TestCase):
    
    def setUp(self):
        self.ip_address = "DicomServer.co.uk"
        self.port = 104
        self.mock_ae = MagicMock()
        self.mock_assoc = MagicMock()
        self.mock_ae.associate.return_value = self.mock_assoc
        self.test_instance = CEcho(self.ip_address, self.port)
    
    def test_verify_association_established(self):
        self.mock_assoc.is_established = True
        self.mock_assoc.send_c_echo.return_value.Status = 0x0000
        
        result = self.test_instance.verify()
        
        self.mock_ae.add_requested_context(Verification).assert_called_once_with(Verification)
        self.mock_ae.associate.assert_called_once_with(self.ip_address, self.port)
        self.mock_assoc.send_c_echo.assert_called_once()
        self.mock_assoc.release.assert_called_once()
        self.assertTrue(result)
        
    def test_verify_association_not_established(self):
        self.mock_assoc.is_established = False
        
        result = self.test_instance.verify()
        
        self.mock_ae.add_requested_context.assert_called_once_with(Verification)
        self.mock_ae.associate.assert_called_once_with(self.ip_address, self.port)
        self.assertFalse(result)
        
    def test_verify_send_c_echo_fails(self):
        self.mock_assoc.is_established = True
        self.mock_assoc.send_c_echo.return_value.Status = 0x0122
        
        result = self.test_instance.verify()
        
        self.mock_ae.add_requested_context.assert_called_once_with(Verification)
        self.mock_ae.associate.assert_called_once_with(self.ip_address, self.port)
        self.mock_assoc.send_c_echo.assert_called_once()
        self.mock_assoc.release.assert_called_once()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()