from utils import run_cmd
from utils import enter_depend_test
enter_depend_test()

from depend_test_framework.core import Action, CheckPoint, ParamsRequire, Provider, Consumer

def migrate_guest(params, env):
    """migrate guest"""
    target_host = params.target_host
    guest_name = params.guest_name
    protocol = params.libvirtd_protocol
    migrate_params = params.migrate_params.live + params.migrate_params.managed + ...

    if migrate_params.find("--xml") != -1 or migrate_params.find("--persistent-xml") != -1:
        "TODO: generate new.xml and new-persistent.xml"
        pass

    cmd = 'virsh migrate %s qemu+%s://%s/system %s' % (guest_name, protocol, target_host, migrate_params)
    ret = run_cmd(cmd)
    params.logger.info("# %s\n%s", cmd, ret)

class migrate(TestObject):
    """ migrate guest"""
    _test_entry = set([Action(1),
                       ParamsRequire(['guest_name', 'target_host']),
                       Consumer('$target_host.$guest_name.active', Consumer.REQUIRE_N)])

    def __init__(self):
        self._test_entry.add(Provider('$target_host.$guest_name.migrated', Provider.SET))

    def __call__(self, params, env):
        migrate_params = params.migrate_params.live + params.migrate_params.managed + ...

        if migrate_params.find("--offline") != -1:
            self.test_entry.add(Consumer('$guest_name.active|$guest_name.config.', Consumer.REQUIRE))
            self.test_entry.add(Provider('$target_host.$guest_name.config', Provider.SET))

        if migrate_params.find("--live") != -1:
            self._test_entry.add(Consumer('$guest_name.active', Consumer.REQUIRE))
            self._test_entry.add(Provider('$target_host.$guest_name.active', Provider.SET))
            self._test_entry.add(Provider('$guest_name.active', Provider.CLEAR))

        if migrate_params.find("--undefinesource") != -1:
            self._test_entry.add(Provider('$guest_name.config', Provider.CLEAR))

        if migrate_params.find("--persistent") != -1:
            self._test_entry.add(Provider('$target_host.$guest_name.config', Provider.SET))

        if migrate_params.find("--tls") != -1:
            self._test_entry.add(Consumer('native_tls_envset', Consumer.REQUIRE))

        if params.libvirtd_protocol == 'ssh':
            self._test_entry.add(Consumer('libvirtd_ssh_envset', Consumer.REQUIRE))

        if params.libvirtd_protocol == 'tcp':
            self._test_entry.add(Consumer('libvirtd_tcp_envset', Consumer.REQUIRE))

        if params.libvirtd_protocol == 'tls':
            self._test_entry.add(Consumer('libvirtd_tls_envset', Consumer.REQUIRE))

        migrate_guest(params, env)

class check_vm_status(TestObject):
    """Check vm status after migration"""
    _test_entry = set([CheckPoint(1)
                       Consumer('$target_host.$guest_name.migrated', Consumer.REQUIRE)])

    def __init__(self):
        pass

class check_vm_status_after_offline_migrate(check_vm_status):
    """Check vm status on source and target host after offline migration: --offline"""
    _test_entry = set(check_vm_status._test_entry)
    _test_entry.add(ParamsRequire(['migrate_params.live == "--offline"'])) // Not sure whether this grammer is supported

    def __init__(self):
        pass

    def __call__(self, params, env):
        "TODO: vm staus should not change on src host after offline migration"
        "TODO: vm should be inactive on target host after offline migration"


class check_vm_status_after_live_migrate(check_vm_status):
    """Check vm status on source and target host after live migration: --live"""
    _test_entry = set(check_vm_status._test_entry)
    _test_entry.add(ParamsRequire(['migrate_params.live == "--live"'])) // Not sure whether this grammer is supported

    def __init__(self):
        pass

    def __call__(self, params, env):
        "TODO: vm should not be active(running or paused) on src host after live migration"
        "TODO: vm should be running on target host after live migration"

class check_migration_port(TestObject):
    """Check the migration port used during live migration""" // Is this kind of parallel operation supported? 
    """# netstat -tunap|grep 491|grep qemu-kvm"""
    _test_entry = set([CheckPoint(1)])

    def __init__(self):
        pass

    def __call__(self, params, env):
        pass
        
class envset(TestObject):
    """setup env before migration"""
    _test_entry = set([Action(1)])

    def __init__(self):
        pass

class native_tls_envset(envset):
    """setup tls env for native tls migration"""
    _test_entry = set(envset._test_entry)
    _test_entry.add(ParamsRequire(['migrate_params.native_tls == "--tls"'])) //Not sure whether this grammer is supported

    def __init__(self):
        super().__init__(self)
        self._test_entry.add(Provider('native_tls_envset', Provider.SET))

    def __call__(self, params, env):
       "TODO: setup native tls migration env"  
       pass

class libvirtd_ssh_envset(envset):
    """ setup ssh env for libvirtd network connectivity"""
    _test_entry = set(envset._test_entry)
    _test_entry.add(ParamsRequire(['libvirtd_protocol == "ssh"'])) //Not sure whether this grammer is supported

    def __init__(self):
        super().__init__(self)
        self._test_entry.add(Provider('libvirtd_ssh_envset', Provider.SET))

    def __call__(self, params, env):
        "TODO: generate sshkey on src host and copy to target host"
        pass

class libvirtd_tls_envset(envset):
    """ setup tls env for libvirtd network connectivity"""
    _test_entry = set(envset._test_entry)
    _test_entry.add(ParamsRequire(['libvirtd_protocol == "tls"'])) //Not sure whether this grammer is supported

    def __init__(self):
        super().__init__(self)
        self._test_entry.add(Provider('libvirtd_tls_envset', Provider.SET))

    def __call__(self, params, env):
        "TODO: RHELAV-8.1: start tls socket, generate tls key and cert"
        "TODO: older version: modify conf file, generate tls key and cert"
        "TODO: enable firewalld port"
        pass

class libvirtd_tcp_envset(envset):
    """ setup tcp env for libvirtd network connectivity"""
    _test_entry = set(envset._test_entry)
    _test_entry.add(ParamsRequire(['libvirtd_protocol == "tcp"'])) //Not sure whether this grammer is supported

    def __init__(self):
        super().__init__(self)
        self._test_entry.add(Provider('libvirtd_tcp_envset', Provider.SET))

    def __call__(self, params, env):
        "TODO: newer version: start tcp socket"
        "TODO: older version: modify conf file"
        "TODO: enable firewalld port"
        pass
