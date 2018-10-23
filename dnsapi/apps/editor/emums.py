from django.utils.translation import ugettext_lazy as _


class RecordClassTypes:
    IN = 'IN'
    CHAOS = 'CH'
    CSNET = 'CS'
    HESIOD = 'HS'

    Choices = (
        (IN, _('the Internet (IN)')),
        (CSNET, _('the CSNET class (CS)')),
        (CHAOS, _('the CHAOS class (CH)')),
        (HESIOD, _('Hesiod (HS)')),
    )


class RecordResourceTypes:
    A = 'A'
    NS = 'NS'
    CNAME = 'CNAME'
    SOA = 'SOA'
    WKS = 'WKS'
    PTR = 'PTR'
    HINFO = 'HINFO'
    MINFO = 'MINFO'
    MX = 'MX'
    TXT = 'TXT'

    Choices = (
        (A, _('a host address (A)')),
        (NS, _('an authoritative name server (NS)')),
        (CNAME, _('the canonical name for an alias (CNAME)')),
        (SOA, _('marks the start of a zone of authority (SOA)')),
        (WKS, _('a well known service description (WKS)')),
        (PTR, _('a domain name pointer (PTR)')),
        (HINFO, _('host information (HINFO)')),
        (MINFO, _('mailbox or mail list information (MINFO)')),
        (MX, _('mail exchange (MX)')),
        (TXT, _('text strings (TXT)')),
    )

class ZoneTypes:
    FWD = 'forward'
    RVS = 'reverse'

    Choices = (
        (FWD, _('forward zone')),
        (RVS, _('reverse zone')),
    )

class ServerTypes:
    BIND9 = 'bind9'

    Choices = (
        (BIND9, _('Bind 9 DNS server')),
    )