import csv, operator


class Data:

    def __init__ (self, source):
        self.source = source

    def __iter__ (self):
        return iter(self.source)

    def _filter (self, f, negate=False):
        def process (source):
            for row in source:
                if f(row) ^ negate:
                    yield row
        return Data(process(self.source))

    def _transform (self, f):
        def process (source):
            for row in source:
                yield f(row)
        return Data(process(self.source))

    def _aggregate (self, f, unpack=False):
        result = set()
        def do_unpack ():
            for row in result:
                yield dict(row)
        for row in self.source:
            f(result, row)
        return Data(do_unpack()) if unpack else result

    def has (self, key, value, op=operator.eq, negate=False):
        return self._filter(lambda row: op(row.get(key), value), negate)

    def unique (self, keys, op=operator.eq):
        if type('') == type(keys):
            return self._aggregate(lambda result, row: result.add(row.get(keys)))
        else:
            return self._aggregate(lambda result, row: result.add(tuple([(key, row.get(key),) for key in keys ])), unpack=True)

    def count (self, keys, new_key='_count', op=operator.eq):

        def do_unpack ():
            for (ref, value) in result.items():
                row = dict(ref)
                row[new_key] = value
                yield row
            
        result = dict()
        for row in self.source:
            ref = []
            for key in keys:
                ref.append((key, row.get(key),))
            ref = tuple(ref)
            if ref in result:
                result[ref] = result[ref] + 1
            else:
                result[ref] = 1

        return Data(do_unpack())


    def cache (self):
        return Data(list(iter(self)))

    def sort (self, key=None, reverse=False):
        return Data(sorted(iter(self.source), key, reverse))


def read_csv(path):
    with open(path, 'r') as file:
        input = csv.DictReader(file)
        for row in input:
            yield row

