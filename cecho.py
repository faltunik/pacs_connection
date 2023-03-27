from pynetdicom import AE
from pynetdicom.sop_class import Verification


class CEcho:

    def __init__(self, ip_address, port) -> None:
        self.ip_address = ip_address
        self.port = port

    def verify(self) -> bool:
        # Initialise the Application Entity
        ae = AE()

        # Add a requested presentation context
        ae.add_requested_context(Verification)

        # Associate with peer AE at IP
        assoc = ae.associate(self.ip_address, self.port)

        if assoc.is_established:
            status = assoc.send_c_echo()
            # check if status means association formed or not
            print('24: STAUTS: ', status, self.ip_address, self.port)
            



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