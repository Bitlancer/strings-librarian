import ldap


def has_tree_changed(ldap_server, base_domain, last_change_timestamp):
    recent_change_found = False

    try:
        for dn, attrs in ldap_server.search_s(base_domain, ldap.SCOPE_SUBTREE, 'objectClass=*', ['*', '+']):
            modify_timestamp = int(attrs['modifyTimestamp'][0][0:-1])
            if modify_timestamp > last_change_timestamp:
                recent_change_found = True
    except ldap.NO_SUCH_OBJECT:
        pass

    return recent_change_found
