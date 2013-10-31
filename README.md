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
    uri=ldap://127.0.0.1
    name=cn=Manager,dc=oasis-infra,dc=net
    pass=mypassword

All fields are required.
