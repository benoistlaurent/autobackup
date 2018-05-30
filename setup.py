
import os
import shutil
import sys

from setuptools import setup
from setuptools.command.install import install


if sys.version_info < (3,):
    sys.exit("Sorry, Python < 3.x is not supported")


SRC_CONFIG_FILE = 'config/workstations.cfg'
DEST_CONFIG_FILE = os.path.join(sys.prefix, 'etc', 'autobackup.cfg')


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self._install_config_file()
        self._print_cron_update_cmd()

    def _install_config_file(self):
        src_config = SRC_CONFIG_FILE
        dest_config = DEST_CONFIG_FILE
        self._mk_config_file_dir(dest_config)
        print("copying {} -> {}".format(src_config, dest_config))
        shutil.copy(src_config, dest_config)

    def _mk_config_file_dir(self, dest_config):
        dirname = os.path.dirname(dest_config)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def _print_cron_update_cmd(self):
        print("To run autobackup every day at 2:00 am, update the crontab:")
        print("0  2    * * *   root    /usr/local/bin/autobackup")


requirements = []
test_requirements = []


setup(
    name='autobackup',
    version='1.0.0',
    description='A simple backup utility',
    author='Benoist LAURENT',
    author_email='benoist.laurent@ibpc.fr',
    url='https://github.com/benoistlaurent/autobackup',
    scripts=['scripts/autobackup'],
    cmdclass={'install': PostInstallCommand}
)


