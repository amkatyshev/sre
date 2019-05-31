class Output(object):
    TO_FILE = 0
    TO_SCREEN = 1

    def __init__(self, outputMode, filename):
        if outputMode == Output.TO_FILE:
            self.__mode__ = Output.TO_FILE
            if isinstance(filename, str):
                self.__filename__ = filename
            else:
                raise AttributeError('Filename must be str type')
        elif outputMode == Output.TO_SCREEN:
            self.__mode__ = Output.TO_SCREEN
        else:
            raise ValueError('Unknown output mode')

    def out(self, data):
        if self.__mode__ == Output.TO_FILE:
            with open(self.__filename__, 'w', encoding='utf8') as file:
                for type, list in data.items():
                    file.write('[' + type + ' relation]\n')
                    if list:
                        for pair in list:
                            file.write(' <-> '.join(pair) + '\n')
                    else:
                        file.write(' -- no concepts --\n')
            print('-- written to file ' + self.__filename__ + ' --')
        elif self.__mode__ == Output.TO_SCREEN:
            for type, list in data.items():
                print('[' + type + ' relation]')
                if list:
                    for pair in list:
                        print(' <-> '.join(pair))
                else:
                    print(' -- no concepts -- ')
        else:
            raise ValueError('Unknown output mode')

