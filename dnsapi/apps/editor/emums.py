from django.utils.translation import ugettext_lazy as _

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