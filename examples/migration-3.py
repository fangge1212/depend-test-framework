from utils import run_cmd
from utils import enter_depend_test
enter_depend_test()

from depend_test_framework.core import Action, CheckPoint, ParamsRequire, Provider, Consumer


class live_migrate_guest(TestObject):
    """live migrate guest"""
    _test_entry = set([Action(1),
                       ParamsRequire.decorator(['guest_name', 'target_host'])])

    def __init__(self):
        self._test_entry.add(Consumer.decorator('$guest_name.active', Consumer.REQUIRE))
        self._test_entry.add(Consumer.decorator('$target_host.$guest_name.active', Consumer.REQUIRE_N))
        self._test_entry.add(Migrate.decorator('guest_name.active', '$target_host.$guest_name.active'))

    def __call_(self, params, env, *args):
        target = params.target_host
        guest_name = params.guest_name
        cmd = 'virsh migrate %s qemu+ssh://%s/system --live %s' % (guest_name, target, ' '.join(args))
        if params.mock:
            params.logger.info("Mock: " + cmd)
            return
        env_setup()
        run_cmd(cmd)

    def env_setup():
        pass
        

class p2p_migrate_guest(live_migrate_guest):
    """p2p migrate guest"""
    _test_entry = set([Action(1),
                       ParamsRequire.decorator(['migrate_options.managed': '--p2p'])])

    def __init__(self):
        super().__init__()

    def __call__(self, params, env, *args):
        env_setup()
        super().__call__(params, env, "--p2p")

    def env_setup():
        super().env_setup()
        pass

class undefinesource_migrate_guest(live_migrate_guest):
    """undefine vm on src in migration process"""
    _test_entry = set([Action(1),
                       ParamsRequire.decorator(['migrate_options.migrate_options': '--undefinesource'])])

    def __init__(self, f):
        self.f = f
        self._test_entry.add(Provider.decorator('$guest_name.config', Provider.CLEAR))

    def __call__(self, params, env):
        super().__call__(params, env, "--undefinesource")
