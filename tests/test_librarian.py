import os
from librarian import librarian
from nose.tools import eq_, raises

DIRNAME = os.path.dirname(os.path.abspath(__file__))

TEST_DATA      = None
TEST_DATA_SIZE = 7

with open ("%s/tfiles/sample_entries.txt" % DIRNAME, "r") as testfile:
    TEST_DATA = eval(testfile.read())


def test_data_available():
    eq_(len(TEST_DATA), TEST_DATA_SIZE)


def test_parse_modify_timestamp():
    timestamp                 = '201310282301Z'
    expected_parsed_timestamp = 201310282301
    actual_parsed_timestamp   = librarian._parse_modify_timestamp(timestamp)

    eq_(expected_parsed_timestamp, actual_parsed_timestamp)


def test_find_forge_tree():
    expected_forge = {
        'url': 'http://forge.puppetlabs.com',
        'path': None,
        'type': 'forge',
        'name': 'bitlancer/ntp',
        'reference': None
    }
    actual_forge = librarian._find_first_forge(TEST_DATA)

    eq_(expected_forge, actual_forge)


def test_parse_forge():
    expected_forge = 'forge "http://forge.puppetlabs.com"\n'
    actual_forge = librarian._parse_forge_entry(librarian._find_first_forge(TEST_DATA))

    eq_(expected_forge, actual_forge)


def test_parse_git_entry():
    git_entry = {
        'name': 'bitlancer/php',
        'path': 'php-fpm/',
        'reference': '5.3',
        'type': 'git',
        'url': 'git://github.com/bitlancer/puppet-php.git'
    }

    expected_entry = 'mod "bitlancer/php"\n\t' + \
                     ',\n\t'.join([':git => "git://github.com/bitlancer/puppet-php.git"',
	                               ':path => "php-fpm/"',
	                               ':ref => "5.3"']) + '\n'
    actual_entry = librarian._parse_nonforge_entry(git_entry)

    eq_(expected_entry, actual_entry)


def test_parse_forge_entry_with_reference():
    forge_entry = {
        'name': 'bitlancer/apache-server',
        'path': None,
        'reference': '2.2',
        'type': 'forge',
        'url': 'http://forge.puppetlabs.com'
    }

    expected_entry = 'mod "bitlancer/apache-server", "2.2"\n'
    actual_entry = librarian._parse_nonforge_entry(forge_entry)

    eq_(expected_entry, actual_entry)


def test_parse_forge_entry_without_reference():
    forge_entry = {
        'name': 'bitlancer/ntp',
        'path': None,
        'reference': None,
        'type': 'forge',
        'url': 'http://forge.puppetlabs.com'
    }

    expected_entry = 'mod "bitlancer/ntp"\n'
    actual_entry = librarian._parse_nonforge_entry(forge_entry)

    eq_(expected_entry, actual_entry)