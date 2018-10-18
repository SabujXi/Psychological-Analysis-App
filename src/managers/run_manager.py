from managers import (
    ManagerOneA,
    ManagerOneB,
    ManagerTwo,
    ManagerThree
)

_managers = {
    'one_a': ManagerOneA,
    'one_b': ManagerOneB,
    'two': ManagerTwo,
    'three': ManagerThree
}


def run_manager(manager_name, root_path, *args, **kwargs):
    # deferreds = []
    # kwargs['deferreds'] = []
    manager_class = _managers[manager_name]
    manager = manager_class(root_path, manager_name, *args, **kwargs)
    manager.run()
    # print manager.deferreds, ' these are the deferreds'
    # for deferred in manager.deferreds:
    #     deferred()
