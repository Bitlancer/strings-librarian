from optparse import OptionParser

from librarian import utils


def main():
    usage = "%prog <ldap_ini> <organization_id>"
    parser = OptionParser(usage=usage)

    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.error("2 args required, %d supplied" % len(args))

    ldap_ini_fname, organization_id = args

    with open(ldap_ini_fname, 'rb') as ldap_ini_file:
        ldap_server = utils.get_ldap_server_for_config(ldap_ini_file)


if __name__ == '__main__':
    main()
