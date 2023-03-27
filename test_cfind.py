import unittest
from unittest.mock import MagicMock
from cfind import CFind
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

class TestMakeRequest(unittest.TestCase):
    
    def setUp(self):
        self.mock_ae = MagicMock()
        self.mock_ae.associate.return_value.is_established = True
        self.mock_ae.add_requested_context.return_value = None
        self.mock_assoc = MagicMock()
        self.mock_ae.associate.return_value = self.mock_assoc
        self.host = "example.com"
        self.port = 1234
        print(self.mock_ae)
        self.test_instance = CFind(self.mock_ae)
    
    def test_make_request(self):
        mock_result = [1, 2, 3]
        self.test_instance.execute_search = MagicMock(return_value=mock_result)
        kwargs = {"patient_id": "12345"}
        expected_result = mock_result
        
        result = self.test_instance.make_request(**kwargs)
        
        self.mock_ae.add_requested_context.assert_called_once_with(PatientRootQueryRetrieveInformationModelFind)
        self.mock_ae.associate.assert_called_once_with(self.host, self.port)
        self.test_instance.execute_search.assert_called_once_with(**kwargs)
        self.mock_assoc.release.assert_called_once()
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    test_obj = TestMakeRequest()
    test_obj.setUp()
    res = test_obj.test_make_request()
    print(res)
    