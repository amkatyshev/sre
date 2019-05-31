class Output(object):
    TO_FILE = 0
    TO_SCREEN = 1

    def __init__(self, outputMode):
        if isinstance(outputMode, str):
            self.__mode__ = Output.TO_FILE
            self.__filename__ = outputMode
        elif outputMode == Output.TO_SCREEN:
            self.__mode__ = Output.TO_SCREEN
        else:
            raise ValueError('Unknown output mode')

    def out(self, data):
        if self.__mode__ == Output.TO_FILE:
            with open(self.__filename__, 'a', encoding='utf8') as file:
                for type, list in data.items():
                    file.write(type + ' relation\n')
                    for pair in list:
                        file.write(' <-> '.join(pair) + '\n')
        elif self.__mode__ == Output.TO_SCREEN:
            for type, list in data.items():
                print(type + ' relation\n')
                for pair in list:
                    print(' <-> '.join(pair) + '\n')
        else:
            raise ValueError('Unknown output mode')

