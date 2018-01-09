import os

import charms_openstack.charm as charm


def install():
    """Use the singleton from the RallyCharm to install the packages on the
    unit
    """
    RallyCharm.singleton.install()


def render_configs(interfaces_list):
    """Using a list of interfaces, render the configs and, if they have
    changes, restart the services on the unit.
    """
    if not os.path.isdir(RallyCharm.RALLY_LOGDIR):
        os.makedirs(RallyCharm.RALLY_LOGDIR)
    RallyCharm.singleton.render_with_interfaces(interfaces_list)
    RallyCharm.singleton.assess_status()


def assess_status():
    """Use the singleton from the RallyCharm to install the packages on the
    unit
    """
    RallyCharm.singleton.assess_status()


def init_db(database):
    """Configure rally with DB connection string, and initialise the DB if 
    it isn't already
    """
    RallyCharm.singleton.configre_db(database)


class RallyCharm(charm.OpenStackCharm):

    release = 'liberty'
    name = 'rally'

    required_relations = ['shared-db']
    """Directories and files used for running rally"""
    RALLY_ROOT = '/var/lib/rally'
    RALLY_LOGDIR = RALLY_ROOT + '/logs'
    RALLY_CONF = RALLY_ROOT + '/rally.conf'

    """List of packages charm should install
    """
    packages = [
        'rally'
    ]

    """Rally has no running services so no services need restarting on
       config file change
    """
    restart_map = {
        RALLY_CONF: [],
    }

    @property
    def all_packages(self):
        _packages = self.packages[:]
        return _packages

    def setup_directories(self):
        for rally_dir in [self.RALLY_ROOT, self.RALLY_LOGDIR]:
            if not os.path.exists(rally_dir):
                os.mkdir(rally_dir)

    def init_db(self, database):
        # write config with DB settings
        # run rally db-recreate, because this should only
        # be run if config changes
        print("erg")
