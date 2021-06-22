from pathlib import Path


class FileIo:

    def __init__(self):
        self.name = 'mdlconfig.txt'
        self.file = Path('.', self.name)

    def dump(self, new_content) -> None:

        with self.file.open(mode='a') as file:
            file.writelines(new_content + '\n')

    def read(self) -> str:

        try:
            with self.file.open() as file:
                contents = file.read()

                if contents == '':
                    print('No contents in file.')

                else:
                    return contents

        except FileNotFoundError:
            print('no file found please create one!')
            return ''

    def create(self) -> None:
        self.file.touch()

    def delete(self) -> None:
        self.file.unlink()
