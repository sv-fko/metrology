from metrology.registry import registry


class Metrology(object):
    @classmethod
    def get(cls, name, tags=None):
        return registry.get(name, tags)

    @classmethod
    def counter(cls, name, tags=None):
        return registry.counter(name, tags)

    @classmethod
    def derive(cls, name, tags=None):
        return registry.derive(name, tags)

    @classmethod
    def meter(cls, name, tags=None):
        return registry.meter(name, tags)

    @classmethod
    def gauge(cls, name, gauge, tags=None):
        return registry.gauge(name, gauge, tags)

    @classmethod
    def timer(cls, name, tags=None):
        return registry.timer(name, tags)

    @classmethod
    def utilization_timer(cls, name, tags=None):
        return registry.utilization_timer(name, tags)

    @classmethod
    def histogram(cls, name, histogram=None, tags=None):
        return registry.histogram(name, histogram, tags)

    @classmethod
    def health_check(cls, name, health_check, tags=None):
        return registry.health_check(name, health_check, tags)

    @classmethod
    def stop(cls):
        return registry.stop()
