from dataclasses import dataclass, field


@dataclass
class Browse:
    #con:dict = {'name':'Browse', 'type':'button', 'label':'Browse', 'event':'on_browse'}
    #server_list: list = ['server1', 'server2', 'server3']
    server_list: list = field(default_factory=lambda: ['server1', 'server2', 'server3'])
    config: dict = field(default_factory=lambda: {'name':'Browse', 'type':'button', 'label':'Browse', 'event':'on_browse'})

    def __init__(self):

        self.arman = 'arman'
        self.print()


    def print(self):
        print(self.config['name'])
        print(self.server_list)

if __name__ == '__main__':
    b = Browse()


