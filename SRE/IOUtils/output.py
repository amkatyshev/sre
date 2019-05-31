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
                file.write(data)
        elif self.__mode__ == Output.TO_SCREEN:
            if isinstance(data, str):
                print(data, end='\n')
            else:
                for line in data:
                    print(line, end='\n')
        else:
            raise ValueError('Unknown output mode')

