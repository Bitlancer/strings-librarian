yum groupinstall "Development Tools"

INSTALL="yum -y install"

$INSTALL python python-devel python-setuptools
$INSTALL openldap-devel

# This seemingly simple sequence of commands in fact took a ton of
# work--getting pip and yum to agree isn't easy.  So, edit at your
# peril.

easy_install pip

# If you get this error: "Wheel installs require setuptools >= 0.8 for dist-info support."
# run the next two cmds with this additional option: "--no-use-wheel"

pip install --upgrade setuptools
pip install --upgrade distribute

pip install python-ldap

# For testing only

pip install nose
