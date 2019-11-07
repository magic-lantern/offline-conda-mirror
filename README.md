# Offline Conda Mirror

Tool for downloading conda packages and all required dependencies for offline use on a different system. While this may work on Windows, it has only been tested on macOS and Linux.

Additionally, this requires Python 3.

## Prerequisites

Install full conda environment on both source and destination systems

## How to use

Suppose you want to setup a Conda environment on a new host with PyTorch, but the host doesn't have Internet access. Normally you would just run: `conda install pytorch torchvision cudatoolkit=10.1 -c pytorch` but that won't work due to outbound Internet not being available.

### On machine with Internet access

Download this repository to a machine that has Internet access. Then run `localmirror.py` and provide appropriate arguments:

```
python ./localmirror.py --help

Usage: localmirror.py [OPTIONS] PACKAGES...

Options:
  --channel <CHANNEL NAME>        Note: multiple --channel options is
                                  supported
  --platform [linux-64|linux-32|osx-64|win-64|win-32]
                                  [default: linux-64]
  --target-directory <TARGET_DIR>
                                  [default: localmirror]
  --help                          Show this message and exit.
```

If you want to download for offline installation PyTorch, you would run the following: `python ./localmirror.py --channel=pytorch pytorch torchvision cudatoolkit=10.1 "python >=3.7,<3.8.0a0"` *Note:* Providing Python version may be helpful but is not always required.

### On machine without Internet access

1. Copy all folders and files downloaded above to new host
1. Add this line to your /etc/hosts file (or modify existing localhost line)
    ```
    127.0.0.1    localhost repo.anaconda.com conda.anaconda.org
    ```
1. Add this line to your ~/.condarc file (create it if it doesn't already exist) - ssl_verify set to false as we are using a self-signed SSL certificate.
    ```
    ssl_verify: false
    ```
1. `cd localmirror`
1. `which python` # substitute your appropriate python including path in next line
1. `sudo python ../https-server.py` # this is required so can listen on port 443 as expected
1. `conda create -n mynewenv python=3.7`
1. `conda activate mynewenv`
1. `conda install pytorch torchvision cudatoolkit=10.1 -c pytorch`
