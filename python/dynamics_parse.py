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
    time = data_run.data()[0]
    raw_pose_data = data_run.data()[3]

    # Splits data by body - this has do do with how the numpy array is formatted
    base_pose = raw_pose_data[:, 0, :]
    mass_pose = raw_pose_data[:, 1, :]  # USE THIS FOR goodtest1
    # mass_pose = raw_pose_data[650:, 1, :]  # Cuts out handheld section of goodtest0-short
    # time = time[650:] # Cuts out handheld section of goodtest0-short

    # Gets X, Y, Z data (all for the rigid body, not the individual markers)
    base_xyz = base_pose[:, 3:]
    mass_xyz = mass_pose[:, 3:]

    # Correct for error
    # There is a shitty data point between 950 and 975 for the base
    # The [950, 975] deletes numbers between those indices, the 0 indicates axis (horizontal)
    # np.delete(base_xyz, [950,975], axis=0)  # Cuts out shitty section of goodtest0-short

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

    # Find peaks
    peak_indices = find_peaks(mass_z)

    # Find R and phi
    R = calculate_r(mass_x, mass_y)
    phi = calculate_phi(R, mass_z)

    # Taken from here: http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#mplot3d-tutorial
    # and this example: http://matplotlib.org/mpl_examples/mplot3d/lines3d_demo.py
    fig1 = plt.figure(1)
    ax = fig1.gca(projection='3d')
    ax.plot([0], [0], [0], marker='o', markersize=10, color='k', label='base')
    # ax.plot(base_xyz[:,0], -base_xyz[:,2], base_xyz[:,1], label='base debuggng')
    ax.plot(mass_x, mass_y, mass_z, color='b', label='mass path')
    ax.plot(mass_x[peak_indices], mass_y[peak_indices], mass_z[peak_indices], 'g.', markersize=10, label='mass path')
    ax.set_xlim3d(-0.5, 0.5)
    ax.set_ylim3d(-0.5, 0.5)
    ax.set_zlim3d(-0.75, 0.25)
    plt.title('Pendulum - Isometric View')
    # ax.legend()
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')

    # top view
    fig2 = plt.figure(2)
    plt.plot([base_x], [base_y], label='base')
    plt.plot(mass_x, mass_y, color='g', label='mass path')
    plt.title('Pendulum - Top View')
    plt.axis([-0.6, 0.6, -0.6, 0.6])
    plt.xlabel('X axis (m)')
    plt.ylabel('Y axis (m)')

    fig3 = plt.figure(3)
    plt.plot(time, phi)
    plt.title('Phi vs. time, where phi is the angle up from the -k axis')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle from vertical (rad)')
    plt.show()


def find_peaks(Z):
    '''
    Returns
      - num_peaks
      - peak_indices
    '''
    peak_indices = []
    check_range = 50  # 25 points on either side of the peak
    for i in range(len(Z)):
        if i <= check_range or i >= len(Z) - check_range:
            pass
        elif sum(Z[i] < Z[i - check_range : i]) == 0 and sum(Z[i] < Z[i + 1 : i + check_range]) == 0:
            peak_indices.append(i)
    return peak_indices


def calculate_phi(R, Z):
    '''
    Returns phi, the angle from -\hat{k}
    '''
    return np.arctan2(R, abs(Z))


def calculate_r(X, Y):
    '''
    Returns R, the radius in cylindrical coordinates
    '''
    return np.sign(X) * np.sqrt(pow(X, 2) + pow(Y, 2))

if __name__ == '__main__':
    main()