import fnmatch
import os
import re


def compile_assets():
    rootPath = './gem/web'
    pattern = '*.js'

    files_to_process = []

    def get_asset_name(path):
        m = re.search('blueprints/(.*?)/', path)
        return m.group(1) + ".js"

    for root, dirs, files in os.walk(rootPath):
        # skip static assets
        if fnmatch.fnmatch(root, "./gem/web/static*"):
            continue

        # get all files
        for filename in fnmatch.filter(files, pattern):
            files_to_process.append(os.path.join(root, filename))

    rmap = {
        file: get_asset_name(file)
        for file in files_to_process
    }
    r = {}
    for key, value in sorted(rmap.items()):
        r.setdefault(value, []).append(key)

    print(r)

    for key, value in r.items():
        with open("./gem/web/static/app/" + key, "w") as af:
            af.write("/* Compiled file, do net edit */\n")

            for path in value:
                af.write("\n\n/* File: {} */\n\n".format(path))
                with open(path, "r") as ff:
                    af.write(ff.read())


if __name__ == "__main__":
    compile_assets()
    print("Assets compiled")