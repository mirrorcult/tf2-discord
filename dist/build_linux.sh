# sudo pip install -r requirements.txt
rm -r tf2disc-linux

cp -r ../src/*.py .
python setup.pyw build
rm *.py

mkdir tf2disc-linux

cp -r build/exe.linux-x86_64-3.8/* tf2disc-linux
cp ../build_files/linux/* tf2disc-linux
cp ../LICENSE tf2disc-linux
cp ../README.md tf2disc-linux

rm -r build