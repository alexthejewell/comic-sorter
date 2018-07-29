class Comic:
    def __init__(self, name):
        self.name = name
        self.fixed_name = self.fix_name(name)
        self.year = self.get_year()
        self.issue_number = self.get_issue_number()
        self.comic_name = self.get_comic_name()

    @staticmethod
    def fix_name(name):
        fixed = name.replace("_", " ")
        return fixed

    def get_year(self):
        pass

    def get_issue_number(self):
        pass

    def get_comic_name(self):
        pass


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
        pass

    def copy_comics(self):
        pass
