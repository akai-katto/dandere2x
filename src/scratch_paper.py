import os, os.path

DIR = 'C:\\Users\\windwoz\\Desktop\\pythonreleases\\0.7\\demo_folder\\weeb\\inputs\\'
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))