# strings-librarian

Bitlancer Strings librarian sync script

## In a Nutshell

A script to sync ou=librarian from LDAP to disk on the Puppet master.  The script should search LDAP, pull in everything under ou=librarian, parse it, and generate a file on disk (see example below).

## Installation

... to be updated by Adam ...

## Configuration

Example configuration:

```
... to be updated by Adam ...
```

All fields are required.

## LDAP to File Translation

The data in LDAP is translated to a file on disk like so:

dn: cn=ntp,ou=puppetlabs,ou=librarian,dc=example,dc=com
description: {"name": "puppetlabs/ntp","type":"forge","url":"http://forge.puppetlabs.com","reference":null,"path":null}

dn: cn=mysql,ou=puppetlabs,ou=librarian,dc=example,dc=com
description: {"name": "puppetlabs/mysql","type":"forge","url":"http://forge.puppetlabs.com","reference":"0.0.3","path":null}

dn: cn=apache,ou=bitlancer,ou=librarian,dc=example,dc=com
description: {"name": "bitlancer/apache","type":"git","url":"git://github.com/bitlancer/bitlancer-apache.git","reference":null,"path":null}

dn: cn=mysql,ou=bitlancer,ou=librarian,dc=example,dc=com
description: {"name": "bitlancer/mysql","type":"git","url":"git://github.com/bitlancer/bitlancer-apache.git","reference":"1.1","path":"feature/great-new-feature"}


becomes:

mod "puppetlabs/ntp" :forge => "http://forge.puppetlabs.com"

mod "puppetlabs/mysql" :forge => "http://forge.puppetlabs.com" :ref => "0.0.3"

mod "bitlancer/apache" :git => "git://github.com/bitlancer/bitlancer-apache.git"

mod "bitlancer/mysql" :git => "git://github.com/bitlancer/bitlancer-apache.git" :ref => "1.1 :path => "feature/great-new-feature"

... on disk.
