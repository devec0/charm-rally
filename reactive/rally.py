import charms.reactive as reactive
import charm.openstack.rally as rally
from charmhelpers.core.hookenv import log, status_set


@reactive.when_not('rally.installed')
def install_rally():
    rally.install()
    reactive.set_state('rally.installed')


@reactive.when('rally.installed')
def assess_status():
    rally.assess_status()


@reactive.when('database.connected')
def setup_database(database):
    rally.configure_db('rally', 'rally')


@reactive.when('database.available')
def use_database(database):
    log("db_host=%s" % database.db_host())
    log("username=%s" % database.username())
    log("password=%s" % database.password())
    log("allowed_units=%s" % database.allowed_units())
    rally.init_db(database)


@reactive.when('database.connected')
@reactive.when_not('database.available')
def waiting_mysql(database):
    status_set('waiting', 'Waiting for MySQL')


@reactive.when('database.connected', 'database.available')
def unit_ready(database):
    # do config render
    status_set('active', 'Unit is ready')
