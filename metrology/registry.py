import inspect

from threading import RLock

from metrology.exceptions import RegistryException, ArgumentException
from metrology.instruments import (
    Counter,
    Derive,
    HistogramUniform,
    Meter,
    Timer,
    UtilizationTimer
)


class Registry(object):
    def __init__(self):
        self.lock = RLock()
        self.metrics = {}

    def clear(self):
        with self.lock:
            for metric in self.metrics.values():
                if hasattr(metric, 'stop'):
                    metric.stop()
            self.metrics.clear()

    def counter(self, name, tags=None):
        return self.add_or_get(name, Counter, tags)

    def meter(self, name, tags=None):
        return self.add_or_get(name, Meter, tags)

    def gauge(self, name, klass, tags=None):
        return self.add_or_get(name, klass, tags)

    def timer(self, name, tags=None):
        return self.add_or_get(name, Timer, tags)

    def utilization_timer(self, name, tags=None):
        return self.add_or_get(name, UtilizationTimer, tags)

    def health_check(self, name, klass, tags=None):
        return self.add_or_get(name, klass, tags)

    def histogram(self, name, klass=None, tags=None):
        if not klass:
            klass = HistogramUniform
        return self.add_or_get(name, klass, tags)

    def derive(self, name, tags=None):
        return self.add_or_get(name, Derive, tags)

    def get(self, name, tags=None):
        with self.lock:
            key = self._compose_key(name, tags)
            return self.metrics[key]

    def add_or_get(self, name, klass, tags=None):
        with self.lock:
            key = self._compose_key(name, tags)
            metric = self.metrics.get(key)
            if metric is not None:
                if not isinstance(metric, klass):
                    raise RegistryException("{0} is not of "
                                            "type {1}.".format(name, klass))
            else:
                if inspect.isclass(klass):
                    metric = klass()
                else:
                    metric = klass
                self.metrics[key] = metric
            return metric

    def stop(self):
        self.clear()

    def _compose_key(self, name, tags=None):
        tags = tags or {}
        if 'name' in tags:
            raise ArgumentException('Tags must not contain a name entry.')
        tags['name'] = name
        return frozenset(tags.items())

    def _decompose_key(self, key):
        tags = {k: v for k, v in key}
        name = tags['name']
        del tags['name']
        tags = tags or None
        return name, tags

    def __iter__(self):
        with self.lock:
            for key, metric in self.metrics.items():
                name, tags = self._decompose_key(key)
                yield name, tags, metric


registry = Registry()
