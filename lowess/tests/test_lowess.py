import numpy as np
import numpy.testing as npt
import lowess as lo


def test_lowess():
    """
    Test 1-d local linear regression with lowess
    """
    np.random.seed(1984)
    for kernel in [lo.epanechnikov, lo.tri_cube]:
        for robust in [True, False]:
            x = np.random.randn(100)
            f = np.sin(x)
            x0 = np.linspace(-1, 1, 10)
            f_hat = lo.lowess(x, f, x0, kernel=kernel, l=1.0, robust=robust)
            f_real = np.sin(x0)
            npt.assert_array_almost_equal(f_hat, f_real, decimal=1)


def test_lowess2d(): 
    """
    Test the 2D case 
    """
    np.random.seed(1977)
    for l in [1.0, 2.0]:
        for kernel in [lo.epanechnikov, lo.tri_cube]:
            for robust in [True, False]:
                for deg in [1, 3]:
                    x = np.random.randn(2, 100)
                    f = -1 * np.sin(x[0]) + 0.5 * np.cos(x[1])
                    x0 = np.mgrid[-1:1:.1, -1:1:.1]
                    x0 = np.vstack([x0[0].ravel(), x0[1].ravel()])
                    f_hat = lo.lowess(x, f, x0, deg=deg, kernel=kernel, l=l,
                                      robust=robust) 
                    f_real = -1 * np.sin(x0[0]) + 0.5 * np.cos(x0[1])
                    npt.assert_array_almost_equal(f_hat, f_real, decimal=0)

    
def test_lowess3d():
    """ 
    Test local linear regression in 3d with lowess
    """
    np.random.randn(2006)
    xyz = np.mgrid[0:1:.1,0:1:.1,0:1:.1]
    x,y,z = xyz[0].ravel(),xyz[1].ravel(),xyz[2].ravel()
    xyz = np.vstack([x,y,z])
    # w = f(x,y,z)
    w = -1 * np.sin(x) + 0.5 * np.cos(y) + np.cos(z)
    
    # Random sample of x,y,z combinations (between -1 and 1):
    xyz0=np.vstack([np.random.rand(2),np.random.rand(2),np.random.rand(2)])     

    # lowess3d is used to find the values at these sampling points:
    w0 = lo.lowess(xyz,w,xyz0)

    # evaluate f(x,y,z) in the uniformly sampled points:
    w0actual =-1 * np.sin(xyz0[0]) + 0.5 * np.cos(xyz0[1]) + np.cos(xyz0[2])
    # This will be undefined in many places 
    npt.assert_array_almost_equal(w0, w0actual, decimal=1)
