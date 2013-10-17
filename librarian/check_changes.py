import ldap


def has_tree_changed(ldap_server, base_domain, last_change_timestamp):
    recent_change_found = False

    try:
        for dn, attrs in ldap_server.search_s(base_domain, ldap.SCOPE_SUBTREE, 'objectClass=*', ['*', '+']):
            modify_timestamp = _parse_modify_timestamp(attrs['modifyTimestamp'][0])
            if modify_timestamp > last_change_timestamp:
                recent_change_found = True
    except ldap.NO_SUCH_OBJECT:
        pass

    return recent_change_found


def _parse_modify_timestamp(timestamp_str):
    timestamp = 0

    if len(timestamp_str) > 0:
        timestamp_str = timestamp_str.rstrip('Z')
        timestamp = int(timestamp_str)

    return timestamp