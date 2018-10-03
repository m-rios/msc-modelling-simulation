import os



root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, 'log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
