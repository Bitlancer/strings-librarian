import time

from optparse import OptionParser

from librarian import librarian, utils


HASHFILE   = '.librarian.hash'
PUPPETFILE = 'Puppetfile'


def main():
    usage = "%prog <ldap_ini> <organization_id>"
    parser = OptionParser(usage=usage)

    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.error("2 args required, %d supplied" % len(args))

    ldap_ini_fname, organization_id = args

    last_hash = utils.get_last_hash(HASHFILE)

    with open(ldap_ini_fname, 'rb') as ldap_ini_file:
        ldap_server = utils.get_ldap_server_for_config(ldap_ini_file)
        tree = utils.select_elements_for_base_domain(ldap_server, organization_id)
        if tree is not None:
            with open(PUPPETFILE, 'w') as puppetfile:
                puppetfile_contents = librarian.generate_puppetfile_from_tree(tree)
                puppetfile.write(puppetfile_contents)
                puppetfile.close()

                puppetfile_digest = utils.get_hex_digest_for(puppetfile_contents)
                if (puppetfile_digest != last_hash):
                    utils.save_last_hash(HASHFILE, puppetfile_digest)


if __name__ == '__main__':
    main()
