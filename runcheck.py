import time

from optparse import OptionParser

from librarian import librarian, utils


TIMESTAMP_FILE   = '.librarian.timestamp'
TIMESTAMP_FORMAT = '%Y%m%d%H%M%S'

PUPPETFILE       = 'Puppetfile'
PUPPETFILE_LOCK  = 'Puppetfile.lock'


def main():
    usage = "%prog <ldap_ini> <organization_id>"
    parser = OptionParser(usage=usage)

    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.error("2 args required, %d supplied" % len(args))

    ldap_ini_fname, organization_id = args

    last_timestamp    = utils.get_last_timestamp(TIMESTAMP_FILE)
    current_timestamp = int(time.strftime(TIMESTAMP_FORMAT))

    with open(ldap_ini_fname, 'rb') as ldap_ini_file:
        ldap_server = utils.get_ldap_server_for_config(ldap_ini_file)
        tree = utils.select_elements_for_base_domain(ldap_server, organization_id)
        if tree is not None and librarian.has_tree_changed(tree, last_timestamp):
            with open(PUPPETFILE, 'w') as puppetfile:
                puppetfile_contents = librarian.generate_puppetfile_from_tree(tree)
                puppetfile.write(puppetfile_contents)
                puppetfile.close()
            utils.save_last_timestamp(TIMESTAMP_FILE, current_timestamp)


if __name__ == '__main__':
    main()
