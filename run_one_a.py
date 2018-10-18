import os
import sys

# env setup
root_path = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.join(root_path, 'src')
sys.path.append(code_path)
os.chdir(code_path)

from managers.run_manager import run_manager
run_manager('one_a', root_path)

