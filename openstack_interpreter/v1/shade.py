from openstack import cloud


class ShadeManager(object):
    """
    """

    def __init__(self, config):
        self.cloud = cloud.openstack_cloud(config=config)
