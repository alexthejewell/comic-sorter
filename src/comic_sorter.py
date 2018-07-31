import re
import shutil


class Comic:
    pattern = r'([a-zA-Z0-9\ \_\-\'\.\!\&\,]+) (\d+\.?\d*).*\((\d+)\).*'

    def __init__(self, name):
        self.name = name
        self.fixed_name = self.fix_name(name)
        self.folder_name = "UNKNOWN"

        match_object = re.match(self.pattern, self.fixed_name)

        if match_object is not None:
            self.comic_name = match_object.group(1)
            self.folder_name = self.comic_name
            self.issue_number = float(match_object.group(2))
            self.year = int(match_object.group(3))

            if self.issue_number.is_integer():
                self.issue_number = int(self.issue_number)
        else:
            self.comic_name = self.fixed_name
            self.issue_number = "unknown"
            self.year = -1
            print("Invalid Comic Name: {}".format(self.name))

    @staticmethod
    def fix_name(name):
        fixed = name.replace("_", " ")
        return fixed


class ComicSorter:
    def __init__(self, source_folder, destination_folder):
        self._src = source_folder
        self._dst = destination_folder
        self._comic_map = dict()
        self._comic_count = 0

    def run(self, folders_only=False, count_only=False):
        self._comic_map = self.build_comic_map(self._src)

        if count_only:
            print("Comic Count: {}".format(self._comic_count))
        elif folders_only:
            self.generate_folders()
        else:
            self.generate_folders()
            self.copy_comics()

    def build_comic_map(self, root_folder):
        comic_map = dict()

        for child in root_folder.iterdir():
            if child.is_dir():
                sub_map = self.build_comic_map(child)
                comic_map.update(sub_map)
            else:
                parsed_comic = self.parse_comic(child)
                comic_map[str(child)] = parsed_comic
                self._comic_count += 1

        return comic_map

    def parse_comic(self, comic_path):
        comic_name = comic_path.name
        parsed_comic = Comic(comic_name)
        return parsed_comic

    def generate_folders(self):
        folder_list = set()
        for comic in self._comic_map.values():
            folder_list.add(comic.folder_name)

        for folder_name in folder_list:
            folder_path = self._dst / folder_name
            if not folder_path.exists():
                folder_path.mkdir()

    def copy_comics(self):
        for comic_path, comic in self._comic_map.items():
            parent_path = self._dst / comic.folder_name
            new_path = parent_path / comic.fixed_name
            if not new_path.exists():
                shutil.copyfile(comic_path, str(new_path))
