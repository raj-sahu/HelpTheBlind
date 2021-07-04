ls -lha kaggle.json
pip install -q kaggle
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 /root/.kaggle/kaggle.json
kaggle datasets download -d watts2/glove6b50dtxt
kaggle datasets download -d shadabhussain/flickr8k
unzip flickr8k
unzip glove6b50dtxt.zip
pwd