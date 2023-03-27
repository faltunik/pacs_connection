from pynetdicom import AE
from pynetdicom.sop_class import Verification

class CEcho:

    def __init__(self, ip_address, port) -> None:
        self.ip_address = ip_address
        self.port = port

    def verify(self) -> bool:
        ae = AE()
        ae.add_requested_context(Verification)
        assoc = ae.associate(self.ip_address, self.port)

        if assoc.is_established:
            status = assoc.send_c_echo()

            if status:
                print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
                return True
            else:
                print('Connection timed out, was aborted or received invalid response')
                assoc.release()
                return False
        else:
            print('Association rejected, aborted or never connected')
            return False