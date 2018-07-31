import sys
from pathlib import Path

from src.comic_sorter import ComicSorter

print(sys.argv)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) not in [3, 4]:
        print("Incorrect number of parameters. Proper usage: comic_sorter <path to find comics> <path to copy comics>")
        print("optional parameter: --folders //only generate folders")
        print("optional parameter: --count //only print a count of comics")
        exit(-1)

    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]

    source = Path(src_dir)
    destination = Path(dst_dir)
    count_only = False
    folders_only = False

    if not source.exists():
        print("Source directory not found: {}".format(source))
        exit(-1)

    if not destination.exists():
        destination.mkdir(parents=True)

    for child in destination.iterdir():
        if child.exists():
            print("Destination directory is not empty")
            exit(-1)

    if len(sys.argv) == 4 and sys.argv[3] == "--folders":
        folders_only = True
    elif len(sys.argv) == 4 and sys.argv[3] == "--count":
        count_only = True

    comic_sorter = ComicSorter(source, destination)
    comic_sorter.run(folders_only, count_only)
