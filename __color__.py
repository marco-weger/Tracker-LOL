from __future__ import print_function
import webcolors
import numpy as np
from scipy.spatial import KDTree
import numpy as np
import binascii
import scipy
import scipy.misc
import scipy.cluster

def getDominant(im):
  NUM_CLUSTERS = 5
  ar = np.asarray(im)
  shape = ar.shape
  ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

  # print('finding clusters')
  codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
  # print('cluster centres:\n', codes)

  vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
  counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

  index_max = scipy.argmax(counts)                    # find most frequent
  peak = codes[index_max]
  colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
  # print('most frequent is %s (#%s)' % (peak, colour))
  return colour

def invertHex(hexNumber):
	#invert a hex number
	inverse = hex(abs(int(hexNumber, 16) - 255))[2:] 
	# if the number is a single digit add a preceding zero
	if len(inverse) == 1: 
		inverse = '0'+inverse
	return inverse

def colorInvert(hexCode):
	#define an empty string for our new colour code
	inverse = "" 
	# if the code is RGB
	if len(hexCode) == 6: 
		R = hexCode[:2]
		G = hexCode[2:4]
		B = hexCode[4:]
	# if the code is ARGB
	elif len(hexCode) == 8:
		A = hexCode[:2]
		R = hexCode[2:4]
		G = hexCode[4:6]
		B = hexCode[6:]
		# don't invert the alpha channel
		inverse = inverse + A 
	else:
		# do nothing if it is neither length
		return hexCode 
	inverse = inverse + invertHex(R)
	inverse = inverse + invertHex(G)
	inverse = inverse + invertHex(B)
	return inverse

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def hexToName(hexCode):
  try:
    return webcolors.hex_to_name(hexCode)
  except ValueError:
    return closest_colour(webcolors.hex_to_rgb(hexCode))