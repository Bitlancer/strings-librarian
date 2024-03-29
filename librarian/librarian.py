import json
import ldap
import utils


def _parse_modify_timestamp(timestamp_str):
    timestamp = 0

    if timestamp_str:
        timestamp_str = timestamp_str.rstrip('Z')
        timestamp = int(timestamp_str)

    return timestamp


def generate_puppetfile_from_tree(tree):
    return '\n'.join([_parse_forge_entry(_find_first_forge(tree))] +
                     [_parse_nonforge_entry(json.loads(obj[1]['description'][0]))
                     for obj in tree
                     if 'description' in obj[1]])


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
    if entry['type'] == 'forge':
        ref_suffix = ', "%s"' % entry['reference']

        return 'mod "%s"%s\n' % (entry['name'], ref_suffix if entry['reference'] else '')
    else:
        mod = entry['name']
        tags = _format_tags_for_entry(entry)
        mod_tags_delim = ""
        if not tags.isspace():
            mod_tags_delim = ','
        return 'mod "%s"%s\n%s\n' % (mod, mod_tags_delim, tags)


def _format_tags_for_entry(tags):
    return ',\n'.join(['\t:%s => "%s"' % (_substitute_tag_name(t), tags[t])
                      for t in tags
                      if t not in ['name', 'type'] and tags[t] is not None])


def _substitute_tag_name(tname):
    if tname == 'url':
        tname = 'git'
    elif tname == 'reference':
        tname = 'ref'

    return tname
