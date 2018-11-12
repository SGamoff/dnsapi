from isc import rndc
from dnsapi.settings.secret import RNDCKEY,RNDCALGO


class ServiceOpertaions:

    def __init__(self, name, port):
        self.service_name = name
        self.service_port = port

    def rndc_reload_service(self):
        try:
            rndc_client = rndc((self.service_name, self.service_port), RNDCALGO, RNDCKEY)
            response = rndc_client.call('status')
            if response['result'] != b'0':
                raise Exception("Error adding zone to master: %s" % response['err'])
            else:
                return response['text']
        except Exception as e:
            return e