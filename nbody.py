#!/usr/bin/env python
import argparse
from gui.MainWindow import MainWindow

def run_default_simulation(n_steps):
    from integrators.integrator import SimRun
    run = SimRun(n_steps=n_steps)
    run.run()


def run_default_gui():
    MainWindow()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform n-body simulations")
    parser.add_argument('-b', '--batch', metavar='n steps', help='run in headless batch mode, ideal for large simulations')
    parser.add_argument('-r', '--replay', metavar='PATH', help='replay a simulation log, for visualization purposes')
    args = parser.parse_args()

    if args.batch is not None:
        run_default_simulation(int(args.batch))
    elif args.replay is not None:
        pass
    else:
        run_default_gui()

