mkdir linux
cp ../build_files/linux/* linux

cp ../LICENSE linux
cp ../README.md linux

sudo pip install -r linux/requirements.txt

python setup.py build