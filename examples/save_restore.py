from utils import enter_depend_test, run_cmd
enter_depend_test()

from depend_test_framework.test_object import Action, CheckPoint, TestObject, Mist, MistDeadEndException, MistClearException, ObjectFailedException, CleanUpMethod
from depend_test_framework.dependency import Provider, Consumer, Migrate, ExtraDepend
from depend_test_framework.base_class import ParamsRequire
from depend_test_framework.test_object import ObjectFailedException


PARAM = {}
ENV = {}


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
# Guest should be active(running or paused) and persistent
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE)
@Consumer.decorator('$guest_name.config', Consumer.REQUIRE)
@Migrate.decorator('$guest_name.active', '$guest_name.managedsaved')
@Provider.decorator('$guest_name.restored', Provider.CLEAR)
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


@CheckPoint.decorator(1)
@Consumer.decorator('$guest_name.managedsaved', Consumer.REQUIRE)
def check_managedsave_guest(params, env):
    """
    Checkpoints after guest is managedsaved
    """
    guest = params.guest_name
    cmd = 'virsh domstate --reason ' + guest
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    ret = run_cmd(cmd)
    params.logger.info("#  %s\n%s", cmd, ret)
    if ret != "shut off (saved)":
        raise ObjectFailedException(CleanUpMethod.not_effect)


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
@Consumer.decorator('$guest_name.managedsaved', Consumer.REQUIRE)
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE_N)
@Migrate.decorator('$guest_name.managedsaved', '$guest_name.active')
@Provider.decorator('$guest_name.restored', Provider.SET)
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


@CheckPoint.decorator(1)
@Consumer.decorator('$guest_name.restored', Consumer.REQUIRE)
def check_restore_guest(params, env):
    """
    Checkpoints after guest is restored from managedsave
    """
    guest = params.guest_name
    cmd = 'virsh domstate --reason ' + guest
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    ret = run_cmd(cmd)
    params.logger.info("# %s\n%s", cmd, ret)
    if ret != "running (restored)":
        raise ObjectFailedException(CleanUpMethod.not_effect)


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
@Consumer.decorator('$guest_name.managedsaved', Consumer.REQUIRE)
@Provider.decorator('$guest_name.managedsaved', Provider.CLEAR)
def remove_managedsave_file(params, env):
    """
    Remove managedsave file
    """
    guest = params.guest_name
    cmd = 'virsh managedsave-remove ' + guest
    ret = run_cmd(cmd)
    params.logger.info("# %s\n%s", cmd, ret)


dep1 = ExtraDepend('start_guest', [Provider('$guest_name.managedsaved', Provider.CLEAR)])
dep2 = ExtraDepend('undefine_guest', [Consumer('$guest_name.managedsaved', Consumer.REQUIRE_N)])
dep3 = ExtraDepend('destroy_guest', [Provider('$guest_name.restored', Provider.CLEAR)])
