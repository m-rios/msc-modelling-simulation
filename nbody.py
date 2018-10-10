#!/usr/bin/env python
import argparse

def run_default_simulation(n_steps, n_stars, name):
    from simulation import SimRun
    run = SimRun(n_steps=n_steps, n_stars=n_stars, name=name)
    run.run()

def run_replay(path):
    from gui.MainWindow import MainWindow
    w = MainWindow()
    w.replay(path)

def run_default_gui(n_stars):
    from gui.MainWindow import MainWindow
    w = MainWindow()
    w.simulate(n_stars=n_stars)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform n-body simulations")
    parser.add_argument('-b', '--batch', metavar='n steps', help='run in headless batch mode, ideal for large simulations')
    parser.add_argument('-r', '--replay', metavar='PATH', help='replay a simulation log, for visualization purposes')
    parser.add_argument('-s', metavar='n stars', help='number of stars to run simulation on', default=10)
    parser.add_argument('-i', metavar='step integrator', help='choose a integrator for the position, velocity, acceleration change of eacth star')
    parser.add_argument('--name', metavar='NAME', help='name of the log file', default="")
    args = parser.parse_args()

    if args.batch is not None:
        print ('default sim')
        run_default_simulation(int(args.batch), int(args.s), args.name)
    elif args.replay is not None:
        print ('replay sim')
        run_replay(args.replay)
    else:
        print ('default gui')
        run_default_gui(int(args.s))

