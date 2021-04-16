class GNS3Project:
    pass

class GNS3Topology:
    pass

class GNS3Node:
    pass

class GNS3Appliance:
    pass

class GNS3ApplianceTemplate:
    pass

class GNS3Drawing:
    pass

class GNS3Adapter:
    pass

class GNS3Port:
    pass

class GNS3Controller:

    def __init__(self, compute_srv=list()):
        self.compute_srv = compute_srv

    def __str__(self):
        return f"A GNS3 controller composed with {str(self.compute_srv)} servers"

class GNS3Compute:
    pass

class GNS3Symbol:
    pass

class GNS3Scene:
    pass

class GNS3Filter:
    pass

c1 = GNS3Controller(["srv_1","srv_2","srv_3"])
print(c1)