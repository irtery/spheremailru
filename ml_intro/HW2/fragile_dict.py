import copy

class FragileDict:
    def __init__(self, data={}):
        self._data = copy.deepcopy(data)
        self._lock = False

    def __contains__(self, value):
        return value in self._data

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if hasattr(self, '_in_context') and self._lock is False:
            self._data[key] = value
            return value
        raise RuntimeError("Protected state")

    def __setattr__(self, name, value):
        if hasattr(self, '_in_context') or name.startswith('_'):
            self.__dict__[name] = value
            return value
        raise RuntimeError("Protected state")

    def __enter__(self):
        self._in_context = True
        self._data_copy = self._data
        self._data = copy.deepcopy(self._data)
        try:
            return self
        except Exception as e:
            err = e  

    def __exit__(self, exc, value, traceback):
        if exc:
            self._data = self._data_copy
        else:
            self._data = copy.deepcopy(self._data)

        for attrname in dir(FragileDict):
            if not attrname.startswith('_'):
                del self.attrname
        del self._data_copy
        del self._in_context
        if exc:
            print("Exception has been suppressed.")
            return True

if __name__ == '__main__':
    d = FragileDict({'key': []})

    with d:
        a = d['key']
        d['key'].append(10)
        a.append(10)

    a.append(10)
    print(a == [10, 10, 10] and d['key'] == [10, 10])