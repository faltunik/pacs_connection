import unittest
from unittest.mock import MagicMock, patch
from cfind import CFind, date_formater, time_formater, serializer, PatientRootQueryRetrieveInformationModelFind, Dataset

class TestHelper(unittest.TestCase):

    def test_date_formater(self):
        # correct
        assert date_formater('20201231') == '2020-12-31'
        #wrong
        assert date_formater('20201231') != '2020-12-32'
        #wrong
        assert date_formater('20201231') != '2020-12-30'

    def test_time_formater(self):
        # correct
        assert time_formater('235959') == '23:59:59'
        # wrong
        assert time_formater('235959') != '23:59:58'
        # wrong
        assert time_formater('235959') != '23:59:60'

    def test_serializer(self):
        obj = [ {'StudyDate': '20201231', 'StudyTime': '235959'} ]
        # correct
        assert serializer(obj) == [ {'StudyDate': '2020-12-31', 'StudyTime': '23:59:59'} ]
        # wrong
        assert serializer(obj) != [ {'StudyDate': '2020-12-31', 'StudyTime': '23:59:58'} ]


class TestCFind(unittest.TestCase):

    @patch('cfind.AE')
    def test_make_request(self, mock_ae):
        #create Mock Objects
        mock_assoc = MagicMock()
        mock_assoc.is_established = True
        mock_ae.associate.return_value = mock_assoc
        execute_search = MagicMock()
        # configure behaviour of execute_search
        execute_search.return_value = [ {'PatientName': 'John Doe', 'PatientID': '123456', 'StudyDate': '20201231', 'StudyTime': '235959'}]


        #create CFind object
        cfind = CFind('localhost', 11112)
        cfind.ae = mock_ae
        cfind.execute_search = execute_search

        #call make_request
        result = cfind.make_request(PatientName='John Doe', PatientID='123456')
        # verify that execute_search was called with correct arguments
        execute_search.assert_called_with(PatientName='John Doe', PatientID='123456')
        # verify that context was added PatientRootQueryRetrieveInformationModelFind
        mock_ae.add_requested_context.assert_called_with(PatientRootQueryRetrieveInformationModelFind)
        #verify that association was established
        mock_ae.associate.assert_called_with('localhost', 11112)
        #verify that association was released
        mock_assoc.release.assert_called_once()
        assert result ==  [ {'PatientName': 'John Doe', 'PatientID': '123456', 'StudyDate': '20201231', 'StudyTime': '235959'}]
        mock_assoc.is_established = False
        result = cfind.make_request(PatientName='John Doe', PatientID='123456')
        assert result == []


    @patch('cfind.AE')
    def test_execute_search(self, mock_ae):

        mock_send_cfind = MagicMock()
        mock_assoc = MagicMock()
        mock_assoc.is_established = True
        mock_ae.associate.return_value = mock_assoc

        cfind = CFind('localhost', 11112)
        cfind.ae = mock_ae
        cfind.send_cfind = mock_send_cfind
        mock_send_cfind.return_value = [ {'PatientName': 'John Doe', 'PatientID': '123456'}]
        mock_dataset = MagicMock()
        mock_dataset.return_value = MagicMock()

        result = cfind.execute_search(PatientID='123456')

        #check whether send_cfind was called with correct argument QueryRetrieveLevel='PATIENT'
        #mock_send_cfind.assert_called_with(PatientID='123456', QueryRetrieveLevel='PATIENT')
        # any call
        print("87", mock_send_cfind.call_args_list)
        #mock_send_cfind.assert_any_call(mock_dataset.return_value, PatientID='123456', QueryRetrieveLevel='PATIENT')

        mock_send_cfind.return_value = [ {'PatientName': 'John Doe', 'PatientID': '123456', 'StudyDate': '20201231', 'StudyTime': '235959'}]
        #mock_send_cfind.assert_called_with(PatientID = '123456', QueryRetrieveLevel = 'STUDY')
        #mock_send_cfind.assert_any_call( PatientID= '123456', QueryRetrieveLevel = 'STUDY') 
        assert mock_send_cfind.call_count == 2
        # result
        assert mock_send_cfind.return_value == [ {'PatientName': 'John Doe', 'PatientID': '123456', 'StudyDate': '20201231', 'StudyTime': '235959'}]

        #TODO
        # Assert whether the fucntion is called with some specific args or not



    @patch('cfind.AE')
    def test_send_cfind(self, mock_ae):
        mock_assoc = MagicMock()
        mock_assoc.is_established = True
        mock_ae.associate.return_value = mock_assoc

        cfind = CFind('localhost', 11112)
        cfind.ae = mock_ae
        cfind.assoc = mock_assoc
        mock_dataset = MagicMock()
        mock_dataset.return_value = MagicMock()

        res = cfind.send_cfind(mock_dataset.return_value, PatientID='123456', QueryRetrieveLevel='PATIENT')

        cfind.create_identifier = MagicMock()

        mock_assoc.send_c_find = MagicMock()
        # return iterator of status, identifier, one None and One some valid identfier 
        mock_assoc.send_c_find.return_value = [ (0x0000, None), (0x0000, Dataset())]


        cfind.create_identifier.assert_called_once
        mock_assoc.send_c_find.assert_called_once


    @patch('cfind.AE')
    def test_create_identifier(self, mock_ae):
        
        # if QueryRetrieveLevel is PATIENT, create_patient_identifier should be called
        cfind = CFind('localhost', 11112)
        cfind.create_patient_identifier = MagicMock()
        cfind.create_study_identifier = MagicMock()
        cfind.create_series_identifier = MagicMock()

        cfind.create_identifier(PatientID='123456', QueryRetrieveLevel='PATIENT')
        cfind.create_patient_identifier.assert_called_once
        cfind.create_study_identifier.assert_not_called
        cfind.create_series_identifier.assert_not_called

        # now change QueryRetrieveLevel to STUDY
        cfind.create_identifier(PatientID='123456', QueryRetrieveLevel='STUDY')
        cfind.create_patient_identifier.assert_called_once
        cfind.create_study_identifier.assert_called_once
        cfind.create_series_identifier.assert_not_called

        # now change QueryRetrieveLevel to SERIES
        cfind.create_identifier(PatientID='123456', QueryRetrieveLevel='SERIES')
        cfind.create_patient_identifier.assert_called_once
        cfind.create_study_identifier.assert_called_once
        cfind.create_series_identifier.assert_called_once

    




        


        




        




if __name__ == '__main__':
    unittest.main()