from utils import STEPS, RESULT, SETUP
import copy

# TODO: use a class for this
DEFAULT = {
    'memory': 1048576,
    'uuid': 'c156ca6f-3c16-435b-980d-9745e1d84ad1',
    'name': 'vm1',
    'id': 1,
}

def managedsave_guest(params, env):
    """
    Managedsave guest
    """
    params.doc_logger.info(STEPS + "# virsh managedsave %s" % params.guest_name)
    params.doc_logger.info(RESULT + "Domain %s state saved by libvirt" % params.guest_name)


def check_managedsave_guest(params, env):
    """
    Checkpoints after guest is managedsaved
    """
    params.doc_logger.info(STEPS + "# virsh domstate --reason %s" % params.guest_name) 
    params.doc_logger.info(RESULT + "shut off (saved)")


def restore_guest_from_managedsaved(params, env):
    """
    Restore guest from managedsave state
    """
    params.doc_logger.info(STEPS + "# virsh start %s" % params.guest_name) 
    params.doc_logger.info(RESULT + "Domain %s started" % params.guest_name)


def check_restore_guest(params, env):
    """
    Checkpoints after guest is restored from managedsave
    """
    params.doc_logger.info(STEPS + "# virsh domstate --reason %s" % params.guest_name) 
    params.doc_logger.info(RESULT + "running (restored)")


def remove_managedsave_file(params, env):
    """
    Remove managedsave file
    """
    pass
