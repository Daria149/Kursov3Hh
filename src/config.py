import os
from configparser import ConfigParser


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_ = os.path.join(project_path, "database.ini")


def config(filename=file_, section="postgresql") -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
        # for param in params:
        #     db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file".format(section, filename))
    print(f"Database parameters: {db}")
    return db


if __name__ == "__main__":
    config()
