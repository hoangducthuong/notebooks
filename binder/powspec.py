import numpy as np

def powspec(image, reso=1):
	"""
	Calculate the power spectrum of a 2D image

	Parameters
	----------
	image : array_like
		Input array, must 2-dimentional and real
	reso : float, optional
		Resolution of the image in pixel^-1

	Returns
	-------

	tab_k : Array of spatial scales used for the decomposition
	spec_k: The power spectrum
	"""
	na=float(image.shape[1])
	nb=float(image.shape[0])
	nf=np.max(np.array([na,nb]))

	k_crit = nf/2    
	k_min = 1

	bins = np.arange(k_crit+1)

	#Fourier transform & 2D power spectrum
	#---------------------------------------------

	imft=np.fft.fft2(image) / (na)
	ps2D = np.abs( imft )**2

	del imft

	#Set-up kbins
	#---------------------------------------------

	x=np.arange(na)
	y=np.arange(nb)
	x,y=np.meshgrid(x,y)

	if (na % 2) == 0:
		x = (1.*x - ((na)/2.) ) / na
		shiftx = (na)/2.
	else:
		x = (1.*x - (na-1)/2.)/ na
		shiftx = (na-1.)/2.+1

	if (nb % 2) == 0:
		y = (1.*y - ((nb/2.)) ) / nb
		shifty = (nb)/2.
	else:
		y = (1.*y - (nb-1)/2.)/ nb
		shifty = (nb-1.)/2+1

	k_mat = np.sqrt(x**2 + y**2)
	k_mat = k_mat * nf 
	#k_mod = np.round(np.fft.fftshift(k_mat),decimals=0)
	
	k_mat= np.roll(k_mat,int(shiftx), axis=1)
	k_mat= np.roll(k_mat,int(shifty), axis=0)
	k_mod = np.round(k_mat,decimals=0)

	hval, rbin = np.histogram(k_mod,bins=bins)

	#Average values in same k bin
	#---------------------------------------------

	kval = np.zeros(np.int(k_crit))
	kpow = np.zeros(np.int(k_crit))

	for j in range(np.int(k_crit)):

		kval[j] = np.sum(k_mod[k_mod == np.float(j)]) / hval[j]
		kpow[j] = np.sum(ps2D[k_mod == np.float(j)]) / hval[j]

	tab_k = kval[1:np.size(hval)-1] / (k_crit * 2.* reso)
	spec_k = kpow[1:np.size(hval)-1]
	
	return tab_k, spec_k