from utils import enter_depend_test, run_cmd
enter_depend_test()

from depend_test_framework.test_object import Action, CheckPoint, TestObject, Mist, MistDeadEndException, MistClearException
from depend_test_framework.dependency import Provider, Consumer, Migrate
from depend_test_framework.base_class import ParamsRequire


PARAM = {}
ENV = {}


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
# Guest should be active(running or paused) and persistent
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE)
@Consumer.decorator('$guest_name.config', Consumer.REQUIRE)
@Migrate.decorator('$guest_name.active', '$guest_name.managedsaved')
def managedsave_guest(params, env):
    """
    Managedsave guest
    """
    guest = params.guest_name
    cmd = 'virsh managedsave ' + guest
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    ret = run_cmd(cmd)
    params.logger.info("# %s\n%s", cmd, ret)


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
@Consumer.decorator('$guest_name.managedsaved', Consumer.REQUIRE)
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE_N)
@Migrate.decorator('$guest_name.managedsaved', '$guest_name.active')
def restore_guest_from_managedsaved(params, env):
    """
    Restore guest from managedsave state
    """
    guest = params.guest_name
    cmd = 'virsh start ' + guest
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    ret = run_cmd(cmd)
    params.logger.info("# %s\n%s", cmd, ret)
