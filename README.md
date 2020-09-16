# mskipkey
Password management tool for Android

# Create a virtual environment
python -m venv path/to/my/venv

## Create e project directory in the virtual environment

# Install kivy and kivyMD
pip install kivy==2.0.0rc3
pip install kivymd

**See [Cython](https://cython.org/)** Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex).

# Install buildozer for Android package
[buildozer documentation](https://buildozer.readthedocs.io/en/latest/)
pip install buildozer

### Install other packages
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

## Init buildozer
buildozer init and configure buildozer settings file: `buildozer.spec`
    
    # (list) Application requirements
    # comma separated e.g. requirements = sqlite3,kivy
    requirements = python3,kivy,kivymd




## First run

buildozer -v android debug

### Warnings
\[WARNING\]: lld not found, linking without it. Consider installing lld if linker errors occur.
