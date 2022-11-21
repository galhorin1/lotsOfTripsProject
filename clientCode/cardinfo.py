import os


filepath = os.path.join(os.getcwd(), "cardData")


def read_file():
    try:
        r = open(filepath, 'r')
        r.close()
    except FileNotFoundError:
        write_file("")
    reader = open(filepath, 'r')
    reader.seek(0)
    return reader.read()


def write_file(d):
    writer = open(filepath, 'w')
    writer.seek(0)
    writer.write("")
    writer.write(d)
    writer.flush()
    writer.close()
