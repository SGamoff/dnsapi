from isc import rndc
from dnsapi.settings.secret import RNDCKEY,RNDCALGO


class ServiceOpertaions:

    def __init__(self, name, port, zone_name):
        self.service_name = name
        self.service_port = port
        self.zone_name = zone_name

    def rndc_reload_service(self):
        try:
            rndc_client = rndc((self.service_name, self.service_port), RNDCALGO, RNDCKEY)
            resp_status_before = rndc_client.call(
                'zonestatus {}'.format(self.zone_name))['text'].decode("utf-8")
            serial_before = self.get_zone_serial(resp_status_before)
            resp_fr = rndc_client.call('freeze {}'.format(self.zone_name))
            if resp_fr['result'] != b'0':
                raise Exception("Error adding zone to master: freeze status - %s"
                                % resp_fr['err'])
            resp_rel = rndc_client.call('reload {}'.format(self.zone_name))
            if resp_rel['result'] != b'0':
                raise Exception("Error adding zone to master: reload status - %s"
                                % resp_rel['err'])
            resp_th = rndc_client.call('thaw {}'.format(self.zone_name))
            if resp_th['result'] != b'0':
                raise Exception("Error adding zone to master: thaw status - %s"
                                % resp_th['err'])
            resp_status_after = rndc_client.call(
                'zonestatus {}'.format(self.zone_name))['text'].decode("utf-8")
            serial_after = self.get_zone_serial(resp_status_after)
            if serial_before == serial_after:
                return 'Zone {} not changed serial - {}'.\
                    format(self.zone_name, serial_after)
            else:
                return 'Zone {} was changed! New serial - {}'.\
                    format(self.zone_name, serial_after)
        except Exception as e:
            return e

    @staticmethod
    def get_zone_serial(text):
        return text[
               text.find('serial:')+8:
               text.find('\n',text.find('serial:'))]
