from Space import *
import argparse
import config as cfg
import visualization
import os

def simulate_exit(plot_values):
    print('Simulation with {}'.format(cfg.image_name))
    space = Space(cfg.width, cfg.height, cfg.nbPeds, imageName=cfg.image_path)
    t = 0
    print(" iteration {} | number of pedestrians left : {}".format(t, space.nbPeds))
    if plot_values:
        visualization.plot_space_with_peds(space, t)
    visualization.plot_sff(space)
    while space.nbPeds != 0:
        t += 1
        conflicts = space.sequential_update()
        space.solveConflicts(conflicts)
        space.updateDFF()
        print(" iteration {} | number of pedestrians left : {}".format(t, space.nbPeds))
        if plot_values:
            visualization.plot_space_with_peds(space, t)
            visualization.plot_dff(space, t)

    return t

def main():

    np.random.seed(0)
    random.seed(0)
    dico = {}
    try:
        total_time = simulate_exit(False)
        dico[cfg.image_name] = total_time
    except:
        pass

    print(dico)

if __name__ == "__main__":
    main()
