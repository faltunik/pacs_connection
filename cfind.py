from pydicom.dataset import Dataset
import time
import json
import datetime

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

debug_logger()

COLS = ["PatientName", "PatientID", "StudyInstanceUID", "SeriesInstanceUID", "StudyDate", "StudyTime", "AccessionNumber", "Modality", "PatientBirthDate", "PatientSex", "PatientAge", "IssuerOfPatientID", "Retrieve AE Title", "StudyDescription"]

def date_formater(s):
    year = s[0:4]
    month = s[4:6]
    day = s[6:8]
    return f"{year}-{month}-{day}"

def time_formater(s):
    try:
        hour = int(s[0:2])
        minute = int(s[2:4])
        second = int(s[4:6])
        return f"{hour}:{minute}:{second}"
    except Exception as e:
        print("ERROR: ", e)
        return s

def serializer(obj):
    # obj: List[Dict]
    for dict_item in obj:
        for key, value in dict_item.items():
            if 'Date' in key:
                dict_item[key] = date_formater(value)
            elif 'Time' in key:
                dict_item[key] = time_formater(value)
    return obj

class CFind:
    """
    TODO: Search via patient name and get all details like patient id, patient name, study date, dob etc
    """

    def __init__(self, host, port, **kwargs):
        print(f"Host : {host} and port: {port}")
        self.host = host
        self.port = port
        self.ae = AE()
        self.user_input = self.get_user_input(**kwargs)
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
        self.mapper = {
            'PATIENT': self.create_patient_identifier,
            'STUDY': self.create_study_identifier,
            'SERIES': self.create_series_identifier,
        }

    def make_request(self, **kwargs):
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
        self.assoc = self.ae.associate(self.host, self.port)
        final_result = []
        if self.assoc.is_established:
            print('HERE 25')
            final_result = self.execute_search(**kwargs)
        
        self.assoc.release()
        
        return final_result
        
    def create_patient_identifier(self, dataset, **kwargs):
        dataset.PatientName = kwargs.get('PatientName', '*')
        dataset.PatientID = kwargs.get('PatientID', '*')
        dataset.PatientBirthDate = kwargs.get('PatientBirthDate', '19000101-99991231')
        # dataset.PatientSex = kwargs.get('PatientSex', 'M')

        return dataset
    
    def create_study_identifier(self, dataset, **kwargs):
        #print(f'STUDY 52: Here we are with kwargs {kwargs} and dataset {dataset} ')
        dataset = self.create_patient_identifier(dataset, **kwargs)
        dataset.StudyInstanceUID = kwargs.get('StudyInstanceUID', '*')
        dataset.StudyDate = kwargs.get('StudyDate', '19000101-99991231')
        #dataset.StudyTime = kwargs.get('StudyTime', '000000.000000-235959.999999')
        #dataset.IssuerOfPatientID = kwargs.get('IssuerOfPatientID', '*')
        #dataset.PatientAge = kwargs.get('PatientAge', '*')
        dataset.AccessionNumber = kwargs.get('AccessionNumber', '*')
        #dataset.Modality = kwargs.get('Modality', '*')
        #dataset.StudyDescription = kwargs.get('StudyDescription', '*'): Giving Connection Aborted Error
        #dataset.InstitutionalDepartmentName = kwargs.get('InstitutionalDepartmentName', '*')
        return dataset
    
    def create_series_identifier(self, dataset, **kwargs):
        dataset = self.create_study_identifier(dataset, **kwargs)
        dataset.SeriesInstanceUID = kwargs.get('SeriesInstanceUID', '*')
        dataset.Modality = kwargs.get('Modality', '*')
        return dataset
    
    def create_identifier(self, dataset= None, **kwargs):
        if not dataset:
            dataset = Dataset()
        #print((kwargs), "71")
        qr_lvl = kwargs.get('QueryRetrieveLevel', 'PATIENT')
        dataset.QueryRetrieveLevel = qr_lvl
        #print(f"FALTUS: {type(self.mapper[qr_lvl](dataset, **kwargs)) }")
        return self.mapper[qr_lvl](dataset, **kwargs)
    
    
    def create_identifier2(self, **kwargs):
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = kwargs.get('QueryRetrieveLevel', 'SERIES')
        if kwargs.get('QueryRetrieveLevel', 'PATIENT') == 'PATIENT':
            if kwargs.get('PatientName'):
                self.ds.PatientName = kwargs.get('PatientName', '*')
                self.ds.PatientID = kwargs.get('PatientID', '*')
        
        if kwargs.get('QueryRetrieveLevel', 'STUDY') == 'STUDY':
            self.ds.PatientName = kwargs.get('PatientName', '*')
            self.ds.PatientID = kwargs.get('PatientID', '*')
            self.ds.StudyInstanceUID = kwargs.get('StudyInstanceUID', '*')
            self.ds.StudyDate = kwargs.get('StudyDate', '*')
            self.ds.StudyTime = kwargs.get('StudyTime', '*')
            self.ds.AccessionNumber = kwargs.get('AccessionNumber', '*')
        
        if kwargs.get('QueryRetrieveLevel', 'SERIES') == 'SERIES':
            self.ds.PatientName = kwargs.get('PatientName', '*')
            self.ds.PatientID = kwargs.get('PatientID', '*')
            self.ds.StudyInstanceUID = kwargs.get('StudyInstanceUID', '*')
            self.ds.SeriesInstanceUID = kwargs.get('SeriesInstanceUID', '*')
            self.ds.Modality = kwargs.get('Modality', '*')
            self.ds.AccessionNumber = kwargs.get('AccessionNumber', '*')

        return self.ds
    
    def get_user_input(self, **kwargs):
        # convert kwargs into dict
        inputs = {}
        for k, v in kwargs.items():
            inputs[k] = v
        return inputs


    def decode_response(self, identifier):
        import collections
        tags = COLS
        #print("identifier", identifier)
        d = collections.defaultdict()
        if not identifier: return {}
        #print(dir(identifier))
        for tag in tags:
            if tag in identifier:
                try:
                    #print(f"{tag}: {identifier.get(tag)}")
                    d[tag] = identifier.get(tag)
                except Exception as e:
                    print(e)
                    continue

        #print("125 identifier", identifier, "dictionary", d)
        return d
    
    def execute_search(self, **kwargs):
        dataset = Dataset()
        #dataset.QueryRetrieveLevel = kwargs.get('QueryRetrieveLevel', 'PATIENT')
        kwargs['QueryRetrieveLevel'] = 'PATIENT'
        patient_output = self.send_cfind(dataset, **kwargs) # List[Dict]
        final_result = []
        for p_op in patient_output:
            #print(f'POP 135: {p_op}')
            n_op = p_op.copy()
            # now make a request with Query Retrieve lvl = Study and PatientID = p_op['PatientID']
            # put this in kwargs
            new_dataset = Dataset()
            nkwargs = kwargs.copy()
            nkwargs['QueryRetrieveLevel'] = 'STUDY'
            if n_op.get('PatientID', False):
                nkwargs['PatientID'] = n_op['PatientID']
            elif n_op.get('PatientName', False):
                nkwargs['PatientName'] = n_op['PatientName']

            study_output = self.send_cfind(new_dataset, **nkwargs)
            for s_op in study_output:
                #print(f"n_op: {n_op} and s_op: {s_op}")
                if s_op != {} or (final_result and final_result[-1] != s_op):
                    f_op = n_op | s_op
                    #print(f_op)
                    final_result.append(f_op)
        print(f'LEN FINAL RESULT: {len(final_result)}')
        #print("156",final_result, "len", len(final_result))
        final_result = serializer(final_result)
        return final_result      



    def send_cfind(self, dataset = Dataset(), **kwargs):
        identifier = self.create_identifier(dataset, **kwargs)
        # print('HERE TYPE1',identifier, identifier.items(), type(identifier))
        #print(f"166: identifier: {identifier}")
        responses = self.assoc.send_c_find(identifier, PatientRootQueryRetrieveInformationModelFind)
        # print('RESPONSE 55', responses, type(responses))
        
        output = []
        count = 0
        for status, res_identifier in responses:
            count +=1
            if status and res_identifier:
                res = self.decode_response(res_identifier)
                if len(res) >0: output.append(res)
                #print("119", res)
                #print(f"for identifier = {identifier} we are getting result nu {count} = {res_identifier} and op = {res}")
            else:
                print('Connection timed out, was aborted or received invalid response')
        return output

if __name__ == '__main__':
    host = ['DicomServer.co.uk', '184.73.255.26']
    port = [104, 11112]
    x = 0
    cfind = CFind(host[x], port[x])
    cfind.make_request()
