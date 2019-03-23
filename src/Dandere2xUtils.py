import os

# waits for a text file, then returns
def wait_on_text(text_file):

    exists = exists = os.path.isfile(text_file)
    while not exists:
        print(text_file, "dne")
        exists = os.path.isfile(text_file)

    file = open(text_file, "r")

    list = file.read().split('\n')
    file.close()

    return list


def main():
    text = wait_on_text("/home/linux/Videos/newdebug/yn2/pframe_data/pframe_1.txt")



if __name__== "__main__":
  main()
