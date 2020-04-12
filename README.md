# bpyconda
Convert any 3D `.obj` file to `.stl`

## Dependency
- Ubunut
- Miniconda
- Python 3.7
- python-blender
- libpn12
- boto3

## How to configure bpyconda

### Step 1: Install miniconda
Goto [conda website](https://docs.conda.io/en/latest/miniconda.html#id3) and download miniconda for `Python 3.7` and `Miniconda Linux 64-bit` for 64 bit ubuntu.

### Step 2: Install libpng12
After `Ubunut 16.04` libpng12 package is update to `libpng16`. For `python-blender` we need libpng12 . To install libpng12 please follow bellow instructions.

Download `libpng12`
```bash
wget https://launchpad.net/~ubuntu-security/+archive/ubuntu/ppa/+build/15108504/+files/libpng12-0_1.2.54-1ubuntu1.1_amd64.deb
```
Install `libpng12`
```bash
sudo dpkg -i libpng12-0_1.2.54-1ubuntu1.1_amd64.deb
```

### Step 3: Install python-blender
To install python-blender use the following instrauctions

Using `conda` package manager
```bash
conda install -c kitsune.one python-blender
```
If failed to install or you got `connection time out error` then install `python-blender` offline. To install it offline use bellow command.
```bash
cd dependency/
conda install python-blender-2.80-1554759302.tar.bz2
```
To check you `python-blender` installation is ok or not go to your python interpreter and `import bpy`. The import of bpy should look like bellow

```bash
Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import bpy
Color management: using fallback mode for management
Color management: scene view "Filmic" not found, setting default "Default".
Color management: scene look "Filmic - Base Contrast" not found, setting default "None".
```
### Step 4: Install boto3
We need `boto3` to access `s3`. Install boto3 using `pip`
```bash
pip install boto3
```
### Step 5: Add 'AWS' credentials
If you want to run it from your local machine you need to add `aws credentials`. 
Add your aws information in the following files in your home directory
```bash
.aws
├── config
└── credentials
```
Now you can run `python convert.py`

### Helps
- [Fixed libpng issue](https://www.linuxuprising.com/2018/05/fix-libpng12-0-missing-in-ubuntu-1804.html)
- [Python blender](https://anaconda.org/kitsune.one/python-blender)
- [Blender python api](https://docs.blender.org/api/current/index.html)
