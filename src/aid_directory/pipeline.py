import csv

def pipeline(*funcs):
    """ Create a reusable function pipeline """
    def inner(data):
        result = data
        for func in funcs:
            result = func(result)
        return result
    return inner

def pipe (arg, *funcs):
    """ Create a temporary pipeline and execute it with a single argument. """
    return pipeline(*funcs)(arg)

def read_csv(path):
    with open(path, 'r') as file:
        input = csv.DictReader(file)
        for row in input:
            yield row

def filter(source, name, values, invert=False):
    if type(values) == type(''):
        values = (values,)
    for row in source:
        if (not invert and row[name] in values):
            yield row
        elif (invert and row[name] not in values):
            yield row

            
def unique(source, keys, include_empty=False):
    """ Generate a sequence of unique values for the keys provided

    If keys is a string, return a sequence of scalars; otherwise,
    return a sequence of dicts.
    """

    result = set()

    # Case 1: a single column: return set of scalars
    if type('') == type(keys):
        for row in source:
            value = row.get(keys)
            if include_empty or value is not None:
                result.add(value)
        return result

    # Case 2: multiple columns: return list of dicts
    else:
        for row in source:
            values = dict()
            for key in keys:
                value = row.get(key)
                if include_empty or value is not None:
                    values[key] = value
            result.add(tuple(values.items()))
        return [dict(item) for item in result]
