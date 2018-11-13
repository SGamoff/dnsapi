#### dnsapi

##### About
This soft is used to manage the DNS server using the django REST API 

##### Requirements
You need dns service worked and configured on server.

##### Installation
1. `pip install -r requirements/base.txt`.
2. `python install requirements/isc/setup.py install` - official module python from https://gitlab.isc.org/isc-projects/bind9.git (folder bin/python)
3. Create database and superuser.

##### BIND9 require configuration:
1. Need create key in named.conf file. Example:
```
key "management-key" {
 	algorithm hmac-sha256;
	secret "secretKey4Management";
};
```
`tsig-keygen` can create this key for you
2. Modified zone must be dynamically and allow update with our key. Example:
```
zone "management-zone" IN {
        type master;
        file "/etc/bind/management-zone.db";
        allow-update { key management-key; };
};
```
3. Add two variables in secret.py project settings folder:
```
RNDCKEY=<content management-key>
RNDCALGO=<algorithm used key creation>
```
