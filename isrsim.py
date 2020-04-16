#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt
import scipy.constants as c

def get_isr_v(N=100,t0=0,t1=1e-3,dt=1e-5,plot_isr_v=False):
    pos=n.zeros([N,3])

    # create N uniform random variable positions
    pos[:,0]=n.random.uniform(0,1.0e3,N)
    pos[:,1]=n.random.uniform(0,1.0e3,N)
    pos[:,2]=n.random.uniform(0,1.0e3,N)+300e3

    # calculate velocity standard deviation
    T=1000.0
    m=16*c.atomic_mass
    vel_std=n.sqrt(c.k*T/m)

    # create normal random variables for velocities
    vel=n.random.randn(N,3)*vel_std

    # scattering k-vector
    k=n.array([0,0,20.0])

    # number of time points
    n_t=int((t1-t0)/dt)
    t=n.arange(n_t)*dt

    # scattered electric field (vector)
    v=n.zeros(n_t,dtype=n.complex64)
    for pi in range(N):
        for ti in range(n_t):
            # trajectory of particle n
            r=n.array([pos[pi,0]+vel[pi,0]*t[ti],
                       pos[pi,1]+vel[pi,1]*t[ti],
                       pos[pi,2]+vel[pi,2]*t[ti]])
            v[ti]+=n.exp(1j*n.dot(k,r))
    if plot_isr_v:
        plt.plot(t/1e-6,v.real)
        plt.plot(t/1e-6,v.imag)
        plt.xlabel("Time ($\mu$s)")
        plt.ylabel("$V(t)$")     
        plt.show()
            
    return(v)

def acf_estimate(N_pulses=1000, N_lags=50, N_scatterers=100, plot_echo_amplitudes=True,dt=1e-5):
    lags=n.arange(0,N_lags)
    acf=n.zeros(len(lags),dtype=n.complex64)

    # simulate N_pulse radar pulses
    for i in range(N_pulses):
        print("radar echo %d/%d"%(i,N_pulses))
        if i == 0:
            v=get_isr_v(N=N_scatterers, t0=0, t1=1e-3, dt=dt,plot_isr_v=True)
        else:
            v=get_isr_v(N=N_scatterers, t0=0, t1=1e-3, dt=dt,plot_isr_v=False)            

        # Estimate all lags via cross-correlation (sample mean estimate)
        for lag,lagi in enumerate(lags):
            # sample mean estimate of the autocorrelation function
            acf[lagi]+=v[0]*n.conj(v[lag])
            
    acf=acf/N_pulses

    # show acf estimate with theoretical 2-sigma error bars
    plt.errorbar(lags*dt/1e-6,acf.real,yerr=2*N_scatterers/n.sqrt(N_pulses),label="Real")
    plt.title("ACF")
    plt.errorbar(lags*dt/1e-6,acf.imag,yerr=2*N_scatterers/n.sqrt(N_pulses),label="Imag")
    plt.xlabel("Lag ($\mu$s)")
    plt.ylabel("Autocorrelation function estimate $\hat{R}(\tau)$")
    plt.title("K=%d"%(N_pulses))
    plt.legend()
    plt.show()


# loop through estimates of the ACF with a
# few different number of measurements (radar pulses)
Np=2
for i in range(14):
    acf_estimate(N_pulses=2**i)

