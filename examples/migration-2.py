from utils import run_cmd
from utils import enter_depend_test
enter_depend_test()

from depend_test_framework.core import Action, CheckPoint, ParamsRequire, Provider, Consumer

add_migrate_options = []

@Action.decorator(1)
@ParamsRequire.decorator(['guest_name', 'target_host'])
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE)
@Consumer.decorator('$target_host.$guest_name.active', Consumer.REQUIRE_N)
@Migrate.decorator('guest_name.active', '$target_host.$guest_name.active')
@p2p_migrate_guest
@undefinesource_migrate_guest
def live_migrate_guest(params, env):
    """live migrate guest"""
    target = params.target_host
    guest_name = params.guest_name
    cmd = 'virsh migrate %s qemu+ssh://%s/system --live %s' % (guest_name, target, " ".join(add_migrate_options))
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    run_cmd(cmd)
        

class p2p_migrate_guest(object):
    """p2p migrate guest"""
    def __init__(self, f):
        self.f = f

    def __call__(self, params, env):
        if params.migrate_options.managed == '--p2p':
            env_setup()
            add_migrate_options.append('--p2p')
        self.f(params, env)

    def env_setup():
        pass

class undefinesource_migrate_guest(object):
    """undefine vm on src in migration process"""
    # how to do f.__test_entry.add(Provider('$guest_name.config', Provider.CLEAR))
    def __init__(self, f):
        self.f = f

    def __call__(self, params, env):
        if params.migrate_options.xxx == '--undefinesource':
            add_migrate_options.append('--undefinesource')
        self.f(params, env)


@CheckPoint.decorator(1)
@ParamsRequire.decorator('migrate_options.xxx': '--undefinesource')
def check_undefinesource_migrate_guest(params, env):
    """check src vm is undefined after migration"""
    pass

