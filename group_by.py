import math
from group import Group


class GroupBy(object):
    def __init__(self) -> None:
        self.group_set = None
        self.groups = None
        self.value_func = None
    
    def create_groups(self, series):
        self.groups = list(map(lambda s: Group(s), series))

    def set_group_set(self, group_set):
        self.group_set = group_set
        return self
    
    def set_value_func(self, value_func):
        self.value_func = value_func
        return self

    def map_group(val) -> int:
        return -1


class RangeGroupBy(GroupBy):
    def __init__(self, start, end, step, format='%s', list=None) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.step = step
        self.create_groups(self.create_series(format, list))

    def map_group(self, val) -> int:
        group_count = len(self.group_set.groups)
        if val < self.start:
            return 0
        if val >= self.end:
            return group_count - 1

        index = math.trunc((val - self.start) / self.step)
        return index + 1

    def create_series(self, format, list) -> list:
        series = ["<" + format % self.start]

        def map_func(n):
            s = n
            e = n + self.step
            label = '%s-%s' % (format % s, format % e)
            return label
        if list:
            series.extend(map(map_func, list))
        else:
            series.extend(
                map(map_func, range(self.start, self.end, self.step)))
        series.append(">=" + format % self.end)

        return series

class ValueGroupBy(GroupBy):
    def __init__(self, values, format='%s') -> None:
        super().__init__()
        self.create_groups(self.create_series(values, format))

    def map_group(self, val) -> int:
        return val

    def create_series(self, values, format) -> list:
        series = []
        series.extend(map(lambda v : format % v, values))
        return series
