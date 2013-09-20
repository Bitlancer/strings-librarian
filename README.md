# strings-librarian

Bitlancer Strings librarian sync script

## In a Nutshell

A script to sync ou=librarian from LDAP to disk on the Puppet master and call librarian-puppet to make the changes live.  

The script should execute something like the following:

* Determine whether any entries have changed. Search ou=librarian for any entries where modifiedTimestamp > the timestamp of the last run. You will need to utilize a local timestamp file.
* If any of the entries have changed, regenerate Puppetfile.
* Generate the Puppetfile configuration on disk per the notes below [LDAP to File Translation](#ldap-to-file-translation).
* If Puppetfile.lock does not exist, call 'librarian-puppet install' else call 'librarian-puppet update' to make the changes live.

Further documentation for librarian here:

https://github.com/rodjek/librarian-puppet/blob/master/README.md


## Installation

... to be updated by Adam ...

## Configuration

Example configuration:

```
... to be updated by Adam ...
```

All fields are required.

## LDAP to File Translation

**Take notice of the different formats for a forge module vs a git module.**

You can make the following assumptions:
* Only one forge will ever be defined. Write the first forge you encounter to the top of the configuration file.
* If type == 'forge', reference will always reflect the version.
* If type == 'forge', path will always be null. Just ignore it.

The data in LDAP is translated to a file on disk like so:

```
dn: cn=ntp,ou=puppetlabs,ou=librarian,dc=example,dc=com
description: {"name": "puppetlabs/ntp","type":"forge","url":"http://forge.puppetlabs.com","reference":null,"path":null}

dn: cn=mysql,ou=puppetlabs,ou=librarian,dc=example,dc=com
description: {"name": "puppetlabs/mysql","type":"forge","url":"http://forge.puppetlabs.com","reference":"0.0.3","path":null}

dn: cn=apache,ou=bitlancer,ou=librarian,dc=example,dc=com
description: {"name": "bitlancer/apache","type":"git","url":"git://github.com/bitlancer/bitlancer-apache.git","reference":null,"path":null}

dn: cn=mysql,ou=bitlancer,ou=librarian,dc=example,dc=com
description: {"name": "bitlancer/mysql","type":"git","url":"git://github.com/bitlancer/bitlancer-apache.git","reference":"1.1","path":"feature/great-new-feature"}
```

becomes:

```
forge "http://forge.puppetlabs.com"

mod "puppetlabs/ntp"

mod "puppetlabs/mysql", "0.0.3"

mod "bitlancer/apache",
  :git => "git://github.com/bitlancer/bitlancer-apache.git"

mod "bitlancer/mysql",
  :git => "git://github.com/bitlancer/bitlancer-apache.git",
  :ref => "1.1",
  :path => "feature/great-new-feature"
```

... on disk.
