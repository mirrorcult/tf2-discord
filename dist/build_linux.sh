mkdir linux
cp ../build_files/install_linux.sh linux
cp ../build_files/open_tf2_rich_presence.sh linux
cp ../build_files/tf2richpresence.service linux
cp ../build_files/uninstall_linux.sh linux

cp ../LICENSE linux
cp ../README.md linux

pyinstaller ../src/main.py -F --clean --distpath linux
mv linux/main linux/tf2-discord

rm -r build
rm main.spec