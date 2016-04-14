import io

class ini:
    class _ini_group:
        def __init__(self, name):
            "Read ini from file object or string given -> ini object"
            self.name = name
            self._items = []
        def __setitem__(self, item, val):
            if type(item) != str:
                raise TypeError("Invalid subscript type")
            for x in range(0, self._items.__len__()):
                if self._items[x][0] == item:
                    self._items[x][1] = val
                    return
            self._items.append([item, val])
        def __getitem__(self, item):
            if type(item) != str:
                raise TypeError("Invalid subscript type")
            for x in range(0, self._items.__len__()):
                if self._items[x][0] == item:
                    return self._items[x][1]
            raise IndexError("Key '" + item + "' not found.")
        def __delitem__(self, item):
            if type(item) != str:
                raise TypeError("Invalid subscript type")
            for x in range(0, self._items.__len__()):
                if self._items[x][0] == item:
                    del self._items[x]
                    return
            raise IndexError("Key '" + item + "' not found.")
        def __iter__(self):
            return iter({x[0]: x[1] for x in self._items if x[0] != -1})
        def __repr__(self):
            return '<ini group {' + (', '.join(['"' + str(x[0]) + '": "' + str(x[1]) + '"' for x in self._items if x[0] != -1])) + '}>'
        def _add_blank_line(self):
            self._items.append([-1, "blankline"])
        def _add_comment(self, comment):
            self._items.append([-1, "comment", comment])
        def _add_raw(self, raw):
            self._items.append([-1, "raw", raw])
    def __init__(self, ini):
        if type(ini) == io.TextIOWrapper:
            if ini.mode == 'r':
                data = ini.read()
                ini.close()
            else:
                raise ValueError('File object does not support reading ("r") mode')
        else:
            if type(ini) == str:
                data = ini
            else:
                raise TypeError('Expected "str" or "io.TextIOWrapper" but got ' + (str(ini.__class__).split()[1][:-1]))
        self._groups = [self._ini_group("__default__")]
        for x in [y.strip() for y in str(data).rsplit(sep='\n')]:
            if x == '':
                self._groups[-1]._add_blank_line()
            elif x[0] == '#':
                self._groups[-1]._add_comment(x[1:])
            elif x[0] == '[':
                self._groups.append(self._ini_group(x[1:-1]))
            elif len(x.split('=', 1)) > 1:
                self._groups[-1][x.split('=', 1)[0].strip()] = x.split('=', 1)[1].strip()
            else:
                self._groups[-1]._add_raw(x)
        self.create_group = self._create_group
        self.dump = self._dump
    def __setitem__(self, item, val):
        raise TypeError("cannot assign to base ini group")  
    def __getitem__(self, item):
        if type(item) != str:
            raise TypeError("Invalid subscript type")
        for x in range(0, self._groups.__len__()):
            if self._groups[x].name == item:
                return self._groups[x]
        raise IndexError("Key '" + item + "' not found.")
    def __delitem__(self, item):
        if type(item) != str:
            raise TypeError("Invalid subscript type")
        for x in range(0, self._groups.__len__()):
            if self._groups[x].name == item:
                del self._groups[x]
                return
        raise TypeError("cannot delete nonexisting ini group.")
    def __iter__(self):
        return iter({x.name: x for x in self._groups})
    def __repr__(self):
        return '<ini group collection [' + (', '.join(['"' + x.name + '"' for x in self._groups])) + ']>'
    def _create_group(self, name):
        for x in range(0, self._groups.__len__()):
            if self._groups[x].name == item:
                raise TypeError("cannot create existing ini group.")
        self._groups.append(self._ini_group(name))
    def _dump(self, stream=None):
        output = []
        for x in self._groups:
            if x.name != '__default__':
                output.append('[' + x.name + ']')
            for y in x._items:
                if (y[0] == -1) and (y[1] == "blankline"):
                    output.append("")
                elif (y[0] == -1) and (y[1] == "comment"):
                    output.append("#" + y[2])
                elif (y[0] == -1) and (y[1] == "raw"):
                    output.append(y[2])
                else:
                    output.append(str(y[0]) + ' = ' + str(y[1]))
        output = '\n'.join(output)
        if stream == None:
            return output
        elif (stream.mode in ['w', 'w+']) and (not stream.closed):
            stream.write(output)
            stream.close()
        elif stream.closed:
            raise IOError('Cannot write to closed stream')
        else:
            raise ValueError('Invalid file mode')
