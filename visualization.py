import matplotlib.pyplot as plt
import numpy as np
import os


def plot_space_with_peds(space, iteration_i=1):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.cla()

    array = np.zeros((len(space.grid), len(space.grid[0])))

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i, j] = space.grid[i][j].state

    cmap = plt.get_cmap("gray")
    cmap.set_bad(color='b', alpha=0.8)

    ax.imshow(array, cmap=cmap, interpolation='nearest', vmin=-1, vmax=2)
    plt.grid(True, color='k', alpha=0.3)
    plt.yticks(np.arange(1.5, array.shape[0], 1))
    plt.xticks(np.arange(1.5, array.shape[1], 1))
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis='both', which='both', length=0)

    S = 't: %3.3d  |  N: %3.3d ' % (iteration_i, space.nbPeds)
    plt.title("%8s" % S)
    figure_name = os.path.join('figures', 'peds', f'peds{iteration_i}.png')
    plt.savefig(figure_name)
    plt.close()


def plot_sff(space):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.cla()

    array = np.zeros((len(space.grid), len(space.grid[0])))

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i, j] = space.grid[i][j].sff_value

    plt.set_cmap('jet')
    cmap = plt.get_cmap()
    cmap.set_bad(color='k', alpha=0.8)

    ax.imshow(array, cmap=cmap, interpolation='nearest', vmin=-1, vmax=2)
    plt.grid(True, color='k', alpha=0.3)
    plt.yticks(np.arange(1.5, array.shape[0], 1))
    plt.xticks(np.arange(1.5, array.shape[1], 1))
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis='both', which='both', length=0)

    plt.title("Static floor field")
    figure_name = os.path.join('figures', 'sff')
    plt.savefig(figure_name)
    plt.close()


def plot_dff(space, iteration_i):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.cla()

    array = np.zeros((len(space.grid), len(space.grid[0])))

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i, j] = space.grid[i][j].dff_value

    plt.set_cmap('jet')
    cmap = plt.get_cmap()
    cmap.set_bad(color='k', alpha=0.8)

    ax.imshow(array, cmap=cmap, interpolation='nearest', vmin=-1, vmax=2)
    plt.grid(True, color='k', alpha=0.3)
    plt.yticks(np.arange(1.5, array.shape[0], 1))
    plt.xticks(np.arange(1.5, array.shape[1], 1))
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis='both', which='both', length=0)

    S = 't: %3.3d ' % (iteration_i)
    plt.title("%8s" % S)
    figure_name = os.path.join('figures', 'dff', 'dff%.6d.png' % iteration_i)
    plt.savefig(figure_name)
    plt.close()
