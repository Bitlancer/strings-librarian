yum groupinstall "Development Tools"

INSTALL="yum -y install"

$INSTALL python python-devel python-setuptools
$INSTALL openldap-devel

# This seemingly simple sequence of commands in fact took a ton of
# work--getting pip and yum to agree isn't easy.  So, edit at your
# peril.

easy_install pip

pip install --upgrade setuptools
pip install --upgrade distribute

pip install python-ldap

# For testing only

pip install nose