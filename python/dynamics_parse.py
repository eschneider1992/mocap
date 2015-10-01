import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from optitrack import Run


def main():
    # Creates the data run object
    data_run = Run()

    # Loads the data using the folder and data name
    data_run.ReadFile('testData', 'goodtest0-short.csv')

    # Gets data in format specified in docstring for data()
    raw_pose_data = data_run.data()[3]

    # Splits data by body - this has do do with how the numpy array is formatted
    base_pose = raw_pose_data[:, 0, :]
    mass_pose = raw_pose_data[:, 1, :]

    # Gets X, Y, Z data (all for the rigid body, not the individual markers)
    base_xyz = base_pose[:, 3:]
    mass_xyz = mass_pose[:, 3:]

    # Correct for error
    # There is a shitty data point between 950 and 975 for the base
    # The [950, 975] deletes numbers between those indices, the 0 indicates axis (horizontal)
    np.delete(base_xyz, [950,975], axis=0)

    # Get average base position
    average_base_pos = np.average(base_xyz, axis=0)

    # Split out individual axes. I did the negative signs and axes because the data
    # came out flipped when there was no transform
    base_x = average_base_pos[0]
    base_y = -average_base_pos[2]
    base_z = average_base_pos[1]
    mass_x = mass_xyz[:,0] - base_x
    mass_y = -mass_xyz[:,2] - base_y
    mass_z = mass_xyz[:,1] - base_z

    # Correct for offsets
    # offset_from_origin = []

    # Taken from here: http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#mplot3d-tutorial
    # and this example: http://matplotlib.org/mpl_examples/mplot3d/lines3d_demo.py
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot([base_x], [base_y], [base_z], label='base')
    ax.plot(mass_x, mass_y, mass_z, color='g', label='mass path')
    ax.set_xlim3d(-0.5, 0.5)
    ax.set_ylim3d(-0.5, 0.5)
    ax.set_zlim3d(-0.75, 0.25)
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()