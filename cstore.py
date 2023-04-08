import time
import json
from dataclasses import dataclass, field
from typing import Any
from pydicom.dataset import Dataset
from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts, debug_logger
import logging


debug_logger()





@dataclass
class CStore:
    """
    Used to Upload DICOM Files to Remote PACS Server
    """
    #TODO: Use Chunking Concept to Upload Large Files
    host: str
    port: int = 4242
    ae: AE = field(default_factory=AE)

    def __post_init__(self)->None:
        self.ae.requested_contexts = StoragePresentationContexts

    def send_c_store(self, path:str)->None:
        ds = dcmread(path)
        #get name of patient name
        patient_name = ds.PatientName
        #get name of study description
        study_description = ds.StudyDescription
        print(f"Patient name is: {patient_name}, Study Description is: {study_description}, File Path is: {path}")
        self.assoc = self.ae.associate(self.host, self.port)
        if self.assoc.is_established:
            status = self.assoc.send_c_store(ds)
            print(status)
            if status:
                print('C-STORE request status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')
            self.assoc.release()
        else:
            print('Association rejected, aborted or never connected')
        return
    


if __name__ == "__main__":
    cstore = CStore("DicomServer.co.uk", 104)
    cstore.send_c_store("testfile.dcm")
    print('DONE REQUEST, Thanks you!')





