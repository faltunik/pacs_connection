from pynetdicom import AE
from pynetdicom.sop_class import Verification

class CEcho:

    def __init__(self, ip_address, port) -> None:
        self.ip_address = ip_address
        self.port = port
        self.ae = AE()
        self.ae.add_requested_context(Verification)
        self.assoc = self.ae.associate(self.ip_address, self.port)

    def verify(self) -> bool:
        if self.assoc.is_established:
            status = self.assoc.send_c_echo()

            if status:
                print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
                self.assoc.release()
                return True
            else:
                print('Connection timed out, was aborted or received invalid response')
                self.assoc.release()
                return False
        else:
            print('Association rejected, aborted or never connected')
            return False