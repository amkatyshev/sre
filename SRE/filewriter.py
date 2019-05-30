class FileWriter(object):
    @staticmethod
    def toFile(data, filename='result.txt', endline='\n', encoding='utf8'):
        with open(filename, 'a', encoding=encoding) as file:
            file.write(data + endline)
