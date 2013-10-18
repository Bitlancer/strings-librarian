from ConfigParser import SafeConfigParser

import ldap


def get_ldap_server_for_config(ldap_ini_file):
    ldap_config_parser = SafeConfigParser()
    ldap_config_parser.readfp(ldap_ini_file)
    ldap_uri = ldap_config_parser.get('sync', 'uri')
    ldap_auth_name = ldap_config_parser.get('sync', 'name')
    ldap_auth_pass = ldap_config_parser.get('sync', 'pass')

    ldap_server = ldap.initialize(ldap_uri)
    ldap_server.simple_bind_s(ldap_auth_name, ldap_auth_pass)

    return ldap_server


def select_elements_for_base_domain(ldap_server, base_domain):
    return ldap_server.search_s(base_domain, ldap.SCOPE_SUBTREE, 'objectClass=*', ['*', '+'])


def get_last_timestamp(filename):
    last_timestamp = 0

    try:
        with open(filename) as file:
            last_timestamp = int(file.readline())
            file.close()
    except IOError:
        pass
    except ValueError:
        pass

    return last_timestamp


def save_last_timestamp(filename, timestamp):
    try:
        with open(filename, 'w') as file:
            file.write(str(timestamp))
            file.close()
    except IOError:
        print 'Error while saving timestamp'
