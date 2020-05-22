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
        self._test_entry.add(Consumer.decorator('env_setup', Consumer.REQUIRE))
        self._test_entry.add(Migrate.decorator('$guest_name.active', '$target_host.$guest_name.active'))

    def __call_(self, params, env):
        target = params.target_host
        guest_name = params.guest_name
        cmd = 'virsh migrate %s qemu+ssh://%s/system --live %s' % (guest_name, target, env.add_options)
        if params.mock:
            params.logger.info("Mock: " + cmd)
            return
        run_cmd(cmd)


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name', 'target_host'])
@Provider.decorator('env_setup', Provider.SET)
def env_setup(params, env):
    """set up env for live migration on both sides, use ssh by default"""
    "TODO:"
    "1. generate ssh-rsa key on both hosts, copy src(dst) ssh key to dst(src) host"
    "2. if firewalld is running, open migration port:49152-49215"
    pass


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name', 'target_host'])
@Provider.decorator('nfs_setup', Provider.SET)
def nfs_setup(params, env):
    """set up nfs storage for live migration on both sides"""
    "TODO:"
    "1. setup nfs server"
    "2. if firewalld is running, open nfs service: firewall-cmd --add-service=nfs"
    "3. if selinux policy is enforcing, setsebool virt_ufs_nfs on"
    pass


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name', 'target_host'])
@Provider.decorator('tls_env_setup', Provider.SET)
def tls_env_setup(params, env):
    """set up tls remote access env on both sides"""
    "1. create cert/key file"
    "2. configure libvirtd for tls access"
    "3. if firewalld is running, open tls port"
    pass


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name', 'target_host'])
@Provider.decorator('tcp_env_setup', Provider.SET)
def tcp_env_setup(params, env):
    """set up tcp remote access env on both sides"""
    "1. configure libvirtd for tls access"
    "2. if firewalld is running, open tcp port"
    pass


class reverse_live_migrate_guest(TestObject):
    """live migrate guest back from dst host to src host"""
    _test_entry = set([Action(1),
                       ParamsRequire.decorator(['guest_name', 'target_host'])])

    def __init__(self):
        self._test_entry.add(Consumer.decorator('$target_host.$guest_name.active', Consumer.REQUIRE))
        self._test_entry.add(Consumer.decorator('$guest_name.active', Consumer.REQUIRE_N))
        self._test_entry.add(Consumer.decorator('env_setup', Consumer.REQUIRE))
        self._test_entry.add(Migrate.decorator('$target_host.$guest_name.active', '$guest_name.active'))

    def __call__(self, params, env):
        target = params.target_host
        guest_name = params.guest_name
        cmd = 'virsh -c qemu+ssh://%s/system migrate %s qemu:///system --live %s' % (target, guest_name)
        if params.mock:
            params.logger.info("Mock: " + cmd)
            return
        run_cmd(cmd)


class p2p_migrate_guest(live_migrate_guest):
    """p2p migrate guest"""
    def __init__(self):
        super(p2p_migrate_guest, self).__init__()

    def __call__(self, params, env):
        add_options = '--p2p'
        super(p2p_migrate_guest, self).__call__(params, env)


class undefinesource_migrate_guest(live_migrate_guest):
    """undefine vm on src host during migration"""
    def __init__(self):
        self._test_entry.add(Provider.decorator('$guest_name.config', Provider.CLEAR))
        super(undefinesource_migrate_guest, self).__init__()

    def __call__(self, params, env):
        env.add_options += '--undefinesource'
        super(undefinesource_migrate_guest, self).__call__(params, env)


class persistent_migrate_guest(live_migrate_guest):
    """make vm persistent(define vm) on dst host during migration"""
    def __init__(self):
        self._test_entry.add(Graft.decorator('$guest_name.active', '$target_host.$guest_name.config'))
        super(persistent_migrate_guest, self).__init__()

    def __call__(self, params, env):
        env.add_options = '--persistent'
        super(persistent_migrate_guest, self).__call__(params, env)


class native_encryption_migrate_guest(live_migrate_guest):
    """encrypt migration data"""
    def __init__(self):
        self._test_entry.add(Consumer.decorator('native_encryption_env_setup', Consumer.REQUIRE))

