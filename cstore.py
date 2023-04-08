import time
import json
import csv
import os
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
    #TODO:Create Spread Sheet to store status of all files so if some files are not uploaded then we can upload them again
    #TODO: Need to handle uploading large number of files

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
        status = None
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
        return status
    
    def upload_full_study(self, folder_path:str)->None:
        # get All files in folder and for each file call send_c_store and if status is success/failed, create a csv files with file path and status(failed/success)

        # so get all files name inside folder
        dummy_name = folder_path.split("/")[-1]
        dummy_name = dummy_name.replace(" ", "_")
        count = 0
        failed = False
        with open(f'upload_results/result_{dummy_name}.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['File Path', 'Status'])
            for file_name in os.listdir(folder_path):
                count +=1
                if count <360: continue
                # create full path
                full_path = os.path.join(folder_path, file_name)
                # call send_c_store
                status = self.send_c_store(full_path)
                # write file path and status to csv file
                writer.writerow([full_path, 'Success' if status else 'Failed'])
                if status:
                    print('C-STORE request status: 0x{0:04x}'.format(status.Status))
                else:
                    failed = True
                    print('Connection timed out, was aborted or received invalid response')
        return failed

    def handle_failed_request(self, report_path:str)->None:
        all_success= True
        updated_rows = []
        with open(report_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for idx, row in enumerate(reader):
                if not row: continue
                file_path = row[0]
                if file_path == 'File Path': continue
                # skip the file if it's already success
                if row[1] == 'Success':
                    updated_rows.append(row)
                    continue
                print(f"Uploading file: {file_path}")
                status = self.send_c_store(file_path)

                # If the upload was successful, update the status in the CSV file
                if status:
                    row[1] = 'Success'
                else:
                    row[1] = 'Failed'
                    all_success = False
                updated_rows.append(row)

        # Write the updated row to the CSV file
        with open(report_path, 'w', newline='') as csv_file:
            fieldnames = ['File Path', 'Status']
            writer = csv.DictWriter(csv_file,delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for row in updated_rows:
                writer.writerow({'File Path': row[0], 'Status': row[1]})
        return all_success

          


if __name__ == "__main__":
    cstore = CStore("DicomServer.co.uk", 104)
    #cstore.upload_full_study("test_file")
    cstore.handle_failed_request("upload_results/result_test_file.csv")
    print('DONE REQUEST, Thanks you!')





