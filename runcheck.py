import time

from optparse import OptionParser

from librarian import check_changes, utils


TIMESTAMP_FILE   = '.librarian.timestamp'
TIMESTAMP_FORMAT = '%Y%m%d%H%M%S'


def get_last_timestamp():
    last_timestamp = 0

    try:
        with open(TIMESTAMP_FILE) as file:
            last_timestamp = int(file.readline())
            file.close()
    except IOError:
        pass
    except ValueError:
        pass

    return last_timestamp


def save_last_timestamp(timestamp):
    try:
        with open(TIMESTAMP_FILE, 'w') as file:
            file.write(str(timestamp))
            file.close()
    except IOError:
        print 'Error while saving timestamp'


def main():
    usage = "%prog <ldap_ini> <organization_id>"
    parser = OptionParser(usage=usage)

    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.error("2 args required, %d supplied" % len(args))

    ldap_ini_fname, organization_id = args

    last_timestamp    = get_last_timestamp()
    current_timestamp = int(time.strftime(TIMESTAMP_FORMAT))

    with open(ldap_ini_fname, 'rb') as ldap_ini_file:
        ldap_server = utils.get_ldap_server_for_config(ldap_ini_file)
        if check_changes.has_tree_changed(ldap_server, organization_id, last_timestamp):
            # TODO: Generate puppetfile
            save_last_timestamp(current_timestamp)


if __name__ == '__main__':
    main()
