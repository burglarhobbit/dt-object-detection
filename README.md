# dt-object-detection
Duckietown Project: Object Detection

## Run inference on the jetson nano

    sudo apt-get install linux-headers-generic build-essential dkms
    sudo apt-get install libffi-dev build-essential git apt-utils 
    sudo apt-get install python-dev python-pip python3-dev python3-pip python3-venv python3-setuptools python3-pkg-resources

    pip3 install cython

Install missing libraries before using pytorch, numpy, scipy:
    sudo apt-get install gfortran libblas-dev liblapack-dev libjpeg-dev zlib1g-dev libopenblas-base libopenmpi2 

Upgrade and install these packages:

pip3 install --upgrade numpy scipy
pip3 install matplotlib, tqdm, Pillow

Download and Install Pytorch==1.6.0 from [this prebuilt binary for Jetpack 4.4/4.4.1](https://nvidia.box.com/shared/static/9eptse6jyly1ggt9axbja2yrmj6pbarc.whl).

Verify Pytorch installation using [these commands](https://stackoverflow.com/a/48152675/5276428).

If error comes during import, install relevant pip libraries.
In case of missing `.so` files, use [apt-file search for missing files](https://stackoverflow.com/questions/63818421/unable-to-import-pytorch-in-jetson-nano-ubuntu)

jetson_clocks turn on:
    sudo jetson_clocks
since `htop` is not available for nano. Use `jtop` after installing this package:
    sudo apt-get install jetson-stats 
