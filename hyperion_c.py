import hyperion
from hyperion.util.constants import *
from hyperion.model import AnalyticalYSOModel
from hyperion.model import ModelOutput 

def run_YSO_model(n_photons, grid, gridnum):
    # Initalize the model
    m = AnalyticalYSOModel()

    # Set the stellar parameters------------------------------------
    m.star.radius = 2. * rsun
    m.star.temperature = 6200.
    m.star.luminosity = 5*lsun
    # Add a flared disk---------------------------------------------
    disk = m.add_flared_disk()
    disk.mass = 0.01 * msun
    disk.rmin = 10 * m.star.radius
    disk.rmax = 200 * au
    disk.r_0 = m.star.radius
    disk.h_0 = 0.01 * disk.r_0
    disk.p = -1.0
    disk.beta = 1.25
    disk.dust = 'kmh_lite.hdf5'
    # Add a powerlaw envelope---------------------------------------
    envelope = m.add_power_law_envelope()
    envelope.mass = 0.4 * msun          # Envelope mass
    envelope.rmin = 200 * au                  # Inner radius
    envelope.rmax = 10000 * au          # Outer radius
    envelope.power = -2                 # Radial power
    envelope.r_0 = disk.rmax

    envelope.dust = 'kmh_lite.hdf5'

    # Use raytracing to improve s/n of thermal/source emission
    m.set_raytracing(True)

    # Use the modified random walk
    m.set_mrw(True, gamma=2.)
    # Set up grid
    m.set_spherical_polar_grid_auto(grid[0], grid[1], grid[2])

    sed = m.add_peeled_images(sed=True, image=False)
    sed.set_viewing_angles([20], [45])
    sed.set_wavelength_range(150, 0.02, 2000.)
    #sed.set_track_origin('basic')

    # Set number of photons
    m.set_n_photons(initial=n_photons, imaging=n_photons,
                    raytracing_sources=n_photons, raytracing_dust=n_photons)

    # Set number of temperature iterations
    m.set_n_initial_iterations(5)
    m.set_convergence(True, percentile=99.0, absolute=2.0, relative=1.1)

    # Write out file
    m.write('N{}grid{}.rtin'.format(n_photons, gridnum), overwrite=True)
    m.run('N{}grid{}.rtout'.format(n_photons, gridnum), overwrite=True)
    return

n_photons = [1e3, 1e4, 1e5, 1e6]
grids = [(100, 50, 2), (200,100,5), (400,200,10)]

for n_photon in n_photons:
    run_YSO_model(n_photon, grids[1], gridnum=1)
    run_YSO_model(n_photon, grids[0], gridnum=0)
    run_YSO_model(n_photon, grids[2], gridnum=2)












