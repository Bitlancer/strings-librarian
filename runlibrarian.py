import os
import subprocess
import time

from optparse import OptionParser

from librarian import librarian, utils


HASHFILE        = '.librarian.hash'
PUPPETFILE      = 'Puppetfile'
PUPPETFILE_LOCK = 'Puppetfile.lock'

MODULE_PATH      = "/etc/puppet/modules"
#MODULE_PATH     = "/etc/puppet/environments/production/modules"

INSTALL_CMD     = "librarian-puppet install --path %s" % MODULE_PATH
UPDATE_CMD      = "librarian-puppet update --path %s" % MODULE_PATH


def main():
    usage = "%prog <ldap_ini> <start_of_librarian_tree>"
    parser = OptionParser(usage=usage)
    parser.add_option("--dry-run",
                      help=("Print the action to be performed, but make no changes"),
                      action="store_true",
                      default=False,
                      dest="dry_run")

    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.error("2 args required, %d supplied" % len(args))

    ldap_ini_fname, librarian_tree = args

    last_hash = utils.get_last_hash(HASHFILE)

    with open(ldap_ini_fname, 'rb') as ldap_ini_file:
        ldap_server = utils.get_ldap_server_for_config(ldap_ini_file)
        tree = utils.select_elements_for_base_domain(ldap_server, librarian_tree)
        if tree is not None:
            with open(PUPPETFILE, 'w') as puppetfile:
                puppetfile_contents = librarian.generate_puppetfile_from_tree(tree)

                if opts.dry_run:
                    print '[Puppetfile]\n%s\n[/Puppetfile]\n\n' % puppetfile_contents,
                else:
                    puppetfile.write(puppetfile_contents)

                puppetfile.close()

                puppetfile_digest = utils.get_hex_digest_for(puppetfile_contents)
                if (puppetfile_digest != last_hash):
                    if opts.dry_run:
                        print 'Changes detected: YES'
                        print 'New hash digest: %s' % puppetfile_digest
                    else:
                        utils.save_last_hash(HASHFILE, puppetfile_digest)

                        if os.path.exists(PUPPETFILE_LOCK):
                            if opts.dry_run:
                                print 'Would call %s' % UPDATE_CMD
                            else:
                                subprocess.call(UPDATE_CMD.split())
                        else:
                            if opts.dry_run:
                                print 'Would call %s' % INSTALL_CMD
                            else:
                                subprocess.call(INSTALL_CMD.split())
                elif opts.dry_run:
                    print 'Changes detected: NO'
                    print 'Previous hash digest: %s' % puppetfile_digest


if __name__ == '__main__':
    main()
