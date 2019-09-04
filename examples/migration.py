from utils import run_cmd
from utils import enter_depend_test
enter_depend_test()

from depend_test_framework.core import Action, ParamsRequire, Provider, Consumer


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name', 'target_host'])
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE)
@Consumer.decorator('$target_host.$guest_name.active', Consumer.REQUIRE_N)
@Provider.decorator('$target_host.$guest_name.active', Provider.SET)
@Provider.decorator('$guest_name.active', Provider.CLEAR)
def migrate(params, env):
    target = params.target_host
    guest_name = params.guest_name
    cmd = 'virsh migrate %s qemu+ssh://%s/system --live' % (guest_name, target)
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    run_cmd(cmd)

class migrate(TestObject):
    """ migrate guest"""
    _test_entry = set([Action(1),
                       ParamsRequire(['guest_name', 'target_host'])])
    def __init__(self):
        self._test_entry.add(Consumer('$target_host.$guest_name.active', Consumer.REQUIRE_N))

class offline_migrate(migrate):
    """ Offline migrate guest"""
    def __init__(self):
        self.test_entry.add(Consumer('$guest_name.active|$guest_name.config.', Consumer.REQUIRE))
        self.test_entry.add(Provider('$target_host.$guest_name.config', Provider.SET))

    def __call__(self, params, env):
        target_host = params.target_host
        guest_name = params.guest_name
        protocol = params.protocol if params.protocol else 'ssh'

        cmd = 'virsh migrate %s qemu+%s://%s/system --offline' % (guest_name, protocol, target_host)
        ret = run_cmd(cmd)
        params.logger.info("# %s\n%s", cmd, ret)

class live_migrate(migrate):
    """ Live migrate guest"""
    def __init__(self):
        self._test_entry.add(Consumer('$guest_name.active', Consumer.REQUIRE)) 
        self._test_entry.add(Provider('$target_host.$guest_name.active', Provider.SET)) 
        self._test_entry.add(Provider('$guest_name.active', Provider.CLEAR)) 

    def __call__(self, params, env):
        target_host = params.target_host
        guest_name = params.guest_name
        protocol = params.protocol if params.protocol else 'ssh'

        cmd = 'virsh migrate %s qemu+%s://%s/system --live' % (guest_name, protocol, target_host)
        ret = run_cmd(cmd)
        params.logger.info("# %s\n%s", cmd, ret)
