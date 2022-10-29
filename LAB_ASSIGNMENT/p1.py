import os

path = './dict'
list = os.listdir(path)
for file in list:
    if os.path.splitext(file)[-1] in ['.html', '.css', '.gif', '.jpg', 'png', '.svg', '.mp3', '.mp4', '.js', '.xml']:
        print(file)