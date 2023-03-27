from pynetdicom import AE
from pynetdicom.sop_class import Verification


class DicomNet:

    def __init__(self) -> None:
        pass


    def cecho(self, **kwargs) -> bool:

        # Create Application Entity
        ae = AE()

        # add presentation context for Verification SOP Class
        ae.add_requested_context(Verification)

        assoc = ae.associate('DicomServer.co.uk', 104)

        if assoc.is_established:
            # Use the C-ECHO service to send the request
            # returns the response status a pydicom Dataset
            status = assoc.send_c_echo()

            # Check the status of the verification request
            if status:
                # If the verification request succeeded this will be 0x0000
                print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
                return True
            else:
                print('Connection timed out, was aborted or received invalid response')

            # Release the association
            assoc.release()

        else:
            print('Association rejected, aborted or never connected')
        return False
    


    def cmove(self, query, **kwargs) -> bool:
        
        pass
    




if __name__ == '__main__':
    dicom_net_obj = DicomNet()
    dicom_net_obj.cecho()