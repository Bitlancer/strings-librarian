import json
import ldap
import utils


def has_tree_changed(tree, last_change_timestamp):
    recent_change_found = False

    try:
        for dn, attrs in tree:
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


def generate_puppetfile_from_tree(tree):
    puppetfile_content = ''

    puppetfile_content += _parse_forge_entry(_find_first_forge(tree)) + '\n'

    for obj in tree:
        attribs = obj[1]

        if 'description' in attribs:
            puppetfile_content += _parse_nonforge_entry(json.loads(attribs['description'][0])) + '\n'

    return puppetfile_content


def _find_first_forge(tree):
    for entry in tree:
        attribs = entry[1]
        if 'description' in attribs:
            parsed_description = json.loads(attribs['description'][0])
            if parsed_description['type'] == 'forge':
                return parsed_description

    return None


def _parse_forge_entry(entry):
    return 'forge "%s"\n' % entry['url']


def _parse_nonforge_entry(entry):
    return 'mod "%s"\n%s\n' % (entry["name"], _format_tags_for_entry(entry))


def _format_tags_for_entry(tags):
    formatted_tags = ''
    for t in tags:
        if t not in ['name', 'type'] and tags[t] != None:
            formatted_tags += '\t:%s => "%s",\n' % (_substitute_tag_name(t), tags[t])

    return formatted_tags.rstrip(',\n')


def _substitute_tag_name(tname):
    if tname == 'url':
        tname = 'git'
    elif tname == 'reference':
        tname = 'ref'

    return tname