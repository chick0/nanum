from os import name
from os import mkdir
from os import listdir
from os.path import join
from os.path import isdir
from os.path import abspath
from os.path import dirname
from os.path import exists
from shutil import rmtree
from zipfile import ZipFile

ROOT_DIR = dirname(abspath(__file__))

BASE_DIR = join(ROOT_DIR, "나눔 글꼴")
WORK_DIR = join(ROOT_DIR, "Fonts")
ZIP_DIR = join(ROOT_DIR, "temp-zip")
D2_DIR = join(ROOT_DIR, "D2Coding")
TEMP_DIR = join(ROOT_DIR, "temp")


def init_dir(dir: str):
    if exists(dir):
        rmtree(dir)

    mkdir(dir)


def copy(a: str, b: str):
    if not exists(b):
        with open(a, mode="rb") as reader:
            with open(b, mode="wb") as writer:
                writer.write(reader.read())


def scan():
    for font in listdir(BASE_DIR):
        FONT_DIR = join(BASE_DIR, font)

        for file in listdir(FONT_DIR):
            FILE_DIR = join(FONT_DIR, file)

            if file.endswith(".woff2") or file.endswith(".woff") or file.endswith(".eot"):
                # Pass web font
                continue

            if "D2Coding" in file:
                for d2 in listdir(FILE_DIR):
                    if d2.endswith(".ttc"):
                        copy(join(FILE_DIR, d2), join(D2_DIR, d2))

                continue

            if isdir(FILE_DIR):
                print("*DIR*", FILE_DIR)
                continue

            if FILE_DIR.endswith(".ttf") or FILE_DIR.endswith(".otf"):
                copy(FILE_DIR, join(WORK_DIR, file))
            elif FILE_DIR.endswith(".zip"):
                copy(FILE_DIR, join(ZIP_DIR, file))
            else:
                print(FILE_DIR)


def unzip():
    for file in listdir(ZIP_DIR):
        FILE_DIR = join(ZIP_DIR, file)

        with ZipFile(FILE_DIR, "r") as zip:
            zip.extractall(TEMP_DIR)


def scan_zip():
    for file in listdir(TEMP_DIR):
        FILE_DIR = join(TEMP_DIR, file)

        if isdir(FILE_DIR):
            for file in listdir(FILE_DIR):
                copy(join(FILE_DIR, file), join(TEMP_DIR, file))

    for file in listdir(TEMP_DIR):
        FILE_DIR = join(TEMP_DIR, file)

        if isdir(FILE_DIR):
            continue

        if FILE_DIR.endswith(".ttf") or FILE_DIR.endswith(".otf"):
            copy(FILE_DIR, join(WORK_DIR, file))
        else:
            print("*ERR*", file)


if __name__ == "__main__":
    init_dir(WORK_DIR)
    init_dir(ZIP_DIR)
    init_dir(D2_DIR)
    init_dir(TEMP_DIR)

    scan()

    unzip()
    scan_zip()

    rmtree(ZIP_DIR)
    rmtree(TEMP_DIR)

    if name == "nt":
        with open(join(ROOT_DIR, "README.txt"), mode="w") as writer:
            writer.write("'Fonts' 풀더안에 있는 폰트 파일을 선택한 다음 우클릭을 눌러 설치를 선택하면 폰트를 설치할 수 있습니다.")
