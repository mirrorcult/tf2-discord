mkdir linux
cp ../build_files/linux/* linux

cp ../LICENSE linux
cp ../README.md linux

sudo pip install -r ../requirements.txt

pyinstaller ../src/main.py --clean --onefile --distpath linux
mv linux/main linux/tf2-discord

rm -r build
rm main.spec
