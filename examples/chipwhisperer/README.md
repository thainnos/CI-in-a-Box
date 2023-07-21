# Chipwhisperer 
This example implements a sidechannel differential power analysis (DPA) attack for an AES implementation with a Chipwhisperer Lite based on the official chipwhisperer example. The whole thing will be executed in a Jenkins pipeline.

## Folder Overview

```bash
├── analyze/    # Scripts for analyze traces 
├── capture/    # Scripts for firmware flashing and trace capturing
├── firmware/   # Sources and makefile to build the target firmware
├── Jenkinsfile # Pipeline Script 
└── README.md   # This file
```

## Requirements
For this example some additional hardware is needed:
- Raspberry Pi 4 (RPi4) or similar edge node device
- Chipwhisperer Lite (CWLite) 32-bit with Cortex-M4 Target

## Description
The example builds the CWLite target firmware on a VM agent, passes it to the RPi4,
flashes the target and captures the power traces.
The captured traces are then passed back to the VM agent, analyzed and compiled into a report.

The firmware itself implements an AES algorithm based on the example provided by the official Chipwhisperer repository.
The analysis attempts to extract the AES key from the captured traces using a DPA attack and
reconstruct it from the attack result.

The example comes with a Jenkinsfile as the pipeline script.
The pipeline consists of 3+2 stages.
The first and last stages are necessary to enable incremental builds.
The 3 main stages - **Build**, **Capture** and **Analyze** - are each only executed when there are changes to the files in the corresponding folders.

| Order | Stage       | Agent     | Note                                                        |
| ----- | ----------- | --------- | ----------------------------------------------------------- |
| 0.    | Prepare     | Ubuntu VM | Prepares the stashes from the artifacts of the previous run |
| 1.    | **Build**   | Ubuntu VM | Build the firmware of the target                            |
| 2.    | **Capture** | RPi4      | Flash the target and capture traces with the CWLite         |
| 3.    | **Analyze** | Ubuntu VM | Analyze the captured traces and generate the report         |
| 4.    | Collect     | Ubuntu VM | Collect all the stashes and save them as artifacts          |

## Setup

### Import the Example
The parent [README](../README.md#importing-an-example-to-gitlab) explains how to import a folder into GitLab.

### Setting up the Jenkins Pipeline
TODO: Setup of RPi and pipeline