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

def restore_guest_from_managedsaved(params, env):
    """
    Restore guest from managedsave state
    """
    params.doc_logger.info(STEPS + "# virsh start %s" % params.guest_name) 
    params.doc_logger.info(RESULT + "Domain %s started" % params.guest_name)
