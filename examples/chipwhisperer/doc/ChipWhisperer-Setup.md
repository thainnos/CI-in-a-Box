# CW meets CI/CD

Angelehnt an die aktuelle [ChipWhisperer Dokumentation](https://chipwhisperer.readthedocs.io/en/latest/linux-install.html) wurden mittels Jenkins-File folgende Pipeline Stages definiert:

- Build Stage
- Test/Capture Stage
- Analyze Stage


## Build Stage
Während der Build Stage wird die Firmware für das ChipWhisperer Lite STM32 Target in einer virtuellen Ubuntu Instanz kompiliert.

```
echo "Build Stage"

// Install required prerequisites for building firmware
sh "sudo apt update"
sh "sudo apt -y install libusb-dev make git avr-libc gcc-avr gcc-arm-none-eabi libusb-1.0-0-dev usbutils"
                
// Build the image
dir("firmware/simpleserial-aes"){
    sh "make PLATFORM=CWLITEARM CRYPTO_TARGET=TINYAES128C"

    // Stash the image
    stash includes: 'simpleserial-aes-CWLITEARM.hex', name: 'image', useDefaultExcludes: false

    // Also archive the image as aritfacts
    archiveArtifacts artifacts: 'simpleserial-aes-CWLITEARM.hex', fingerprint: true, onlyIfSuccessful: true
}
```    
## Test Stage
Die Test Stage wird auf dem Raspberry Pi ausgeführt. 
Anschließend wird ein Capture Skript ausgeführt, welches mithilfe des ChipWhisperer Frameworks die ChipWhisperer Lite Hardware anspricht und die Stromaufnahme des STM32-Targets aufzeichnet.

```
echo 'Test Stage'

// Clean up workspace
cleanWs(deleteDirs: true, patterns:[[pattern: '.pyenv/**', type: 'EXCLUDE']])

// Checkout the git into the src subdir
dir("src"){
  checkout scm
}

// Unstash the previous image
dir("src/capture/image"){
  unstash 'image'
}

// Install required packages for pyenv
sh "sudo apt-get update"
sh """
sudo apt-get install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
sudo apt install -y build-essential gdb lcov pkg-config \
libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
lzma lzma-dev tk-dev uuid-dev zlib1g-dev curl
"""

// Install pyenv
// If .pyenv dir exists (and therefore pyenv) just update it, else install it
sh "if [ -d .pyenv ]; then pyenv update; else curl https://pyenv.run | bash; fi"
sh "pyenv init -"
sh "pyenv virtualenv-init -"

// Install python versions
sh "pyenv install -s $REQ_PYTHON_VER_WITH_MINOR"
sh "pyenv global $REQ_PYTHON_VER_WITH_MINOR"

withPythonEnv("$HOME/.pyenv/shims/${PYTHON_CMD}"){
  // Debug
  sh "$PYTHON_CMD --version"

  dir("src/capture"){
    // Set up chipwhisperer
    sh """
    sudo cp 50-newae.rules /etc/udev/rules.d/50-newae.rules
    sudo udevadm control --reload-rules
    sudo usermod -aG dialout $USER
    sudo usermod -aG plugdev $USER
    $PYTHON_CMD -m pip install chipwhisperer
    """
    // Run the script
    sh """
    $PYTHON_CMD capture.py
    """
  }
}

dir("src/capture"){
// Stashing the results 
stash includes: 'trace_array.npy, textin_array.npy, known_keys.npy', name: 'captures', useDefaultExcludes: false
// Also archive the results as aritfacts
archiveArtifacts artifacts: 'trace_array.npy, textin_array.npy, known_keys.npy', fingerprint: true, onlyIfSuccessful: true
}
```

### Capture Skript

```python
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

############################
# Program the STM32 Target #
############################
cw.program_target(scope, prog, "./image/simpleserial-aes-{}.hex".format(PLATFORM))

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
```


## Analyze Stage
Abschließend werden in einer Analyse Stage, welche wieder in einer virtuellen Ubuntu VM ausgeführt wird, die aufgezeichneten Power Traces ausgewertet. 

```
echo "Analyze Stage"

// Install dependencies
sh """
sudo apt install -y python3-pip python3-venv pandoc \
texlive-xetex texlive-fonts-recommended texlive-plain-generic
"""

dir("analyze"){

  // Unstash the results from the capturing
  dir("captures"){
    unstash 'captures'
  }
                    
  withPythonEnv("python3"){
    // Install the python libs
    sh "pip install -r requirements.txt"

    // Run the analyze script
    sh "python3 analyze_traces.py"

    // Build the notebooks to html
    sh "jupyter nbconvert --execute cw_analysis_results_nb.ipynb --to html"
    // sh "jupyter nbconvert --execute cw_analysis_results_nb.ipynb --to pdf"
    // sh "jupyter nbconvert --execute cw_analysis_results_nb.ipynb --to webpdf"
    // sh "jupyter nbconvert --execute cw_analysis_results_nb.ipynb --to slides"
    // sh "jupyter nbconvert --execute cw_analysis_results_nb.ipynb --to latex"
  }

  // Archive the rendered jupyter as aritfacts
  archiveArtifacts artifacts: 'cw_analysis_results_nb.html', fingerprint: true, onlyIfSuccessful: true
  // archiveArtifacts artifacts: 'cw_analysis_results_nb.pdf', fingerprint: true, onlyIfSuccessful: true
}
```

### Analyze Traces Skript
```python
from tqdm.notebook import tnrange
import numpy as np


##################################
# Load Captured Traces from Disk #
##################################
trace_array = np.load('./captures/' +
                      'trace_array.npy')
textin_array = np.load('./captures/' +
                       'textin_array.npy')
known_keys = np.load('./captures/' +
                     'known_keys.npy')

num_traces = np.shape(trace_array)[0]  # total number of traces
num_points = np.shape(trace_array)[1]  # samples per trace
known_key = known_keys[0]



##############################
# Prepare and Start Analysis #
##############################
num_subkeys = 16
sbox = (0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b,
        0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26,
        0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2,
        0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed,
        0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f,
        0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
        0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14,
        0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d,
        0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f,
        0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11,
        0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f,
        0xb0, 0x54, 0xbb, 0x16)

def intermediate(pt, keyguess):
    return sbox[pt ^ keyguess]

# Calculate the difference of means and pick the right guess
key_guesses = np.empty([num_subkeys])

mean_diffs = np.zeros(255)
global_mean_diffs = np.empty([num_subkeys, 255])
global_mean_diffs_hex = np.chararray([num_subkeys, 255], itemsize=4, unicode=True)

plots = np.empty([255, num_points])
global_plots = np.empty([num_subkeys, num_points])
color_mask = np.empty([num_subkeys, 255])

# separating traces into different groups based on the SBox's output
# based on the least significant bit (but really any bit would work)
for subkey in tnrange(0, num_subkeys, desc="Attacking Subkey"):
    for kguess in tnrange(255, desc="Keyguess", leave=False):
        one_list = []
        zero_list = []

        for tnum in range(num_traces):
            if (intermediate(textin_array[tnum][subkey], kguess) & 1):
                # LSB is 1
                one_list.append(trace_array[tnum])
            else:
                zero_list.append(trace_array[tnum])

        # calculate the difference of means
        one_avg = np.asarray(one_list).mean(axis=0)
        zero_avg = np.asarray(zero_list).mean(axis=0)
        mean_diffs[kguess] = np.max(abs(one_avg - zero_avg))
        plots[kguess] = abs(one_avg - zero_avg)

    # collect data for every subkey
    global_plots[subkey] = plots[mean_diffs.argsort()][-1]
    global_mean_diffs[subkey] = np.flip(np.sort(mean_diffs))
    mean_diffs_hex = [hex(i) for i in np.flip(np.argsort(mean_diffs))]
    # global_mean_diffs[subkey] = np.flip(np.sort(mean_diffs))[:255]
    # mean_diffs_hex = [hex(i) for i in np.flip(np.argsort(mean_diffs))[:255]]
    global_mean_diffs_hex[subkey] = mean_diffs_hex

    # create mask for box plot
    color_mask[subkey] = [
        1 if hex_value == hex(known_key[subkey]) else 0
        for hex_value in mean_diffs_hex
    ]

    # repeat with each possible key guess
    # then pick the one with the highest difference of means
    guess = np.argsort(mean_diffs)[-1]
    key_guesses[subkey] = guess
    print(hex(guess) + "(real = 0x{:02x})".format(known_key[subkey]))

print(len(global_plots))
print(global_mean_diffs)
print(global_mean_diffs_hex)

########################
# Save Results to Disk #
########################
np.save('./results/global_plots.npy', global_plots)
np.save('./results/global_mean_diffs.npy', global_mean_diffs)
np.save('./results/global_mean_diffs_hex.npy', global_mean_diffs_hex)
np.save('./results/key_guesses.npy', key_guesses)
np.save('./results/color_mask.npy', color_mask)
```