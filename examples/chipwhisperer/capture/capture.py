#!/home/ubuntu/.pyenv/versions/cw/lib/python3.9

import chipwhisperer as cw
import time
from tqdm import tnrange, trange
import numpy as np
import subprocess

SCOPETYPE = 'OPENADC'
PLATFORM = 'CWLITEARM'
CRYPTO_TARGET='TINYAES128C'


############################
# Connect to ChipWhisperer #
############################

try:
    if not scope.connectStatus:
        scope.con()
except NameError:
    scope = cw.scope()
   
try:
    target = cw.target(scope)
except IOError:
    print("INFO: Caught exception on reconnecting to target - attempting to reconnect to scope first.")
    print("INFO: This is a work-around when USB has died without Python knowing. Ignore errors above this line.")
    scope = cw.scope()
    target = cw.target(scope)

print("INFO: Found ChipWhisperer")


###########################
# Target Programmer Setup #
###########################

if "STM" in PLATFORM or PLATFORM == "CWLITEARM" or PLATFORM == "CWNANO":
    prog = cw.programmers.STM32FProgrammer
elif PLATFORM == "CW303" or PLATFORM == "CWLITEXMEGA":
    prog = cw.programmers.XMEGAProgrammer
else:
    prog = None


###############
# Scope Setup #
###############

time.sleep(0.05)
scope.default_setup()
def reset_target(scope):
    if PLATFORM == "CW303" or PLATFORM == "CWLITEXMEGA":
        scope.io.pdic = 'low'
        time.sleep(0.05)
        scope.io.pdic = 'high_z' #XMEGA doesn't like pdic driven high
        time.sleep(0.05)
    else:  
        scope.io.nrst = 'low'
        time.sleep(0.05)
        scope.io.nrst = 'high'
        time.sleep(0.05)


##################################
# Compile and Program the Target #
##################################

# subprocess.run(["make", "PLATFORM=CWLITEARM", "CRYPTO_TARGET=TINYAES128C"], cwd="../hardware/victims/firmware/simpleserial-aes")

cw.program_target(scope, prog, "./image/simpleserial-aes-{}.hex".format(PLATFORM))


###################
# Holoviews Setup #
###################

# import holoviews as hv
# from holoviews.streams import Pipe, Buffer
# import pandas as pd
# 
# class real_time_plot:
#     def __init__(self, plot_len):
#         hv.extension('bokeh')
#         st = pd.DataFrame({'y':[]}, columns=['y'])
#         self.dfstream = Buffer(st, length=plot_len, index=False)
#         curve_dmap = hv.DynamicMap(hv.Curve, streams=[self.dfstream])
#         curve_dmap.opts(width=800, height=600)
#         display(curve_dmap)
#     def send(self, data):
#         if hasattr(data, 'wave'):
#             d = data.wave
#         else:
#             d = data
#         self.dfstream.send(pd.DataFrame({'y':d}))
# 
# plot = real_time_plot(plot_len=3000) # Open Holoviews Plot


##################
# Capture Traces #
##################

ktp = cw.ktp.Basic()

traces = []
N = 250  # Number of traces

if PLATFORM == "CWLITEARM" or PLATFORM == "CW308_STM32F3":
    scope.adc.samples = 4000
elif PLATFORM == "CWLITEXMEGA" or PLATFORM == "CW303":
    scope.gain.db = 20
    scope.adc.samples = 1700 - 170
    scope.adc.offset = 500 + 700 + 170
    N = 5000
    
print(scope)
for i in trange(N, desc='Capturing traces'):
    key, text = ktp.next()  # manual creation of a key, text pair can be substituted here

    trace = cw.capture_trace(scope, target, text, key)
    if trace is None:
        continue
    traces.append(trace)
#    plot.send(trace)


scope.dis()
target.dis()

##################################
# Convert Traces to numpy arrays #
# Save Captured Traces to Disk   #
##################################

trace_array = np.asarray([trace.wave for trace in traces])
textin_array = np.asarray([trace.textin for trace in traces])
known_keys = np.asarray([trace.key for trace in traces])  # for fixed key, these keys are all the same

np.save('trace_array.npy', trace_array)
np.save('textin_array.npy', textin_array)
np.save('known_keys.npy', known_keys)

print("INFO: Saved Captured Traces")
