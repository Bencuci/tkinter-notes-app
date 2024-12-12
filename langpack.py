import glob

class I18N:
    def __init__(self, lang):
        if lang in self.get_available_languages():
            self.trn = self.load_data_from_file(lang)
        else:
            raise NotImplementedError("Language not supported")

    @staticmethod
    def load_data_from_file(lang):
        with open(f"languages/{lang}.lang", "r", encoding="utf-8") as f:
            return dict([x.strip().split("=") for x in f.readlines()])

    @staticmethod
    def get_available_languages():
        return [x.split("/")[1].split(".")[0] for x in glob.glob("languages/*.lang")]
