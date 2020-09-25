from .file_parser import BabelFiler
from googletrans import Translator

def translate(src_file, output_file, trans_lang):
    text_material = BabelFiler(src_file=src_file, output_file=output_file,
                               trans_lang=trans_lang)

    lines = text_material.read_file(src_file)
    babel = Translator()
    babel.detect(lines)

    text_material.make_file()

    text_material.write_to_file(babel.translate("".join(lines),
                                             dest=trans_lang).text)
    return "Done"

