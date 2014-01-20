# strings-librarian

Bitlancer Strings librarian sync script

## Installation

1. Install dependencies:
> $ ./install_deps.sh

2. Edit `ldap.ini` to match the run-time environment
3. Configure `cron` to execute `runlibrarian.sh` at the desired interval

## Configuration

Example configuration:

*ldap.ini*

    [sync]
    uri=ldap://dsa01.dfw01.socius.strings-service.net
    name=uid=librarian,ou=users,ou=ldap,dc=example-infra,dc=net
    pass=mypassword

All fields are required.
