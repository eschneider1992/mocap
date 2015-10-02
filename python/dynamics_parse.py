import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from optitrack import Run


def main():
    # Creates the data run object
    data_run = Run()

    # Loads the data using the folder and data name
    # data_run.ReadFile('testData', 'goodtest0-short.csv')
    data_run.ReadFile('testData', 'goodtest1.csv')
    
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
    # np.delete(base_xyz, [950,975], axis=0)

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

    # Find peaks
    peak_indices = find_peaks(mass_z)
    print("peak_indices: ")
    print(peak_indices)

    # Taken from here: http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#mplot3d-tutorial
    # and this example: http://matplotlib.org/mpl_examples/mplot3d/lines3d_demo.py
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot([base_x], [base_y], [base_z], label='base')
    ax.plot(mass_x, mass_y, mass_z, color='g', label='mass path')
    # ax.plot()
    ax.set_xlim3d(-0.5, 0.5)
    ax.set_ylim3d(-0.5, 0.5)
    ax.set_zlim3d(-0.75, 0.25)
    ax.legend()
    plt.show()


def find_peaks(Z):
    '''
    Returns
      - num_peaks
      - peak_indices
    '''
    peak_indices = []
    check_range = 25  # 25 points on either side of the peak
    for i in range(len(Z)):
        if i <= check_range or i >= len(Z) - check_range:
            pass
        elif sum(Z[i - check_range : i] < Z[i]) == 0 and sum(Z[i] < Z[i + 1 : i + check_range]) == 0:
            print("Found a local maximum at i = %d", i)
            peak_indices.append(i)
        elif sum(Z[i - check_range : i] > Z[i]) == 0 and sum(Z[i] > Z[i + 1 : i + check_range]) == 0:
            print("Found a local minimum at i = %d", i)
            peak_indices.append(i)
    return peak_indices


if __name__ == '__main__':
    main()