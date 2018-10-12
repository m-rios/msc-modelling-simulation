#!/usr/bin/env python
import argparse
import simulation
from simulation import Euler, Leapfrog, Hermite
from model import Universe


def run_batch(args):
    from simulation import SimRun
    u = Universe(n_stars=args.s, mass=args.m)
    run = SimRun(n_steps=args.n, universe=u, name=args.name)
    run.run()


def run_replay(args):
    from gui.MainWindow import MainWindow
    sim = simulation.Player(args.replay)
    w = MainWindow(sim)
    w.simulate()


def run_gui(args):
    from gui.MainWindow import MainWindow
    integrators = {'euler':Euler(), 'leapfrog':Leapfrog(), 'hermite':Hermite()}
    try:
        integrator = integrators[args.integrator]
    except:
        print("Integrator must one of: euler, leapfrog, hermite")
        exit(-1)
    sim = simulation.SimRun(n_steps=args.n, n_stars=args.s, integrator=integrator)
    w = MainWindow(sim)
    w.simulate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform n-body simulations")
    parser.add_argument('-b', '--batch', action='store_true', help='run in headless batch mode, ideal for large simulations')
    parser.add_argument('-r', '--replay', metavar='PATH', help='replay a simulation log, for visualization purposes')
    parser.add_argument('-s', metavar='STARS', help='number of stars to run simulation on', default=10, type=int)
    parser.add_argument('-n', metavar='STEPS', help='number of steps to run simulation for', default=200, type=int)
    parser.add_argument('--name', metavar='NAME', help='name of the log file', default="")
    parser.add_argument('-i', '--integrator', metavar='step integrator', help='choose a integrator for the position, velocity, acceleration change of eacth star', default='euler')
    parser.add_argument('-m', metavar='MASS', help='The mass of each star', default=1e5, type=float)
    args = parser.parse_args()

    if args.batch:
        print('Running in batch mode')
        run_batch(args)
    elif args.replay is not None:
        print('Replaying simulation')
        run_replay(args)
    else:
        print('Running in visual mode')
        run_gui(args)
