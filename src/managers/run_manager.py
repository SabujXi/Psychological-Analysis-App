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
    manager_class = _managers[manager_name]
    manager = manager_class(root_path, manager_name, *args, **kwargs)
    manager.run()
