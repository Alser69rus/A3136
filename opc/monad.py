class Maybe:
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error

    def __call__(self, func, *args, **kwargs):
        if not (self.value is None):
            try:
                v = func(self.value, *args, **kwargs)
                return Maybe(value=v, error=None)
            except Exception as exc:
                return Maybe(value=None, error=exc)
        return self

    def __repr__(self):
        if not (self.value is None):
            return 'Just {}'.format(self.value)
        else:
            return 'Nothing ({})'.format(self.error)

    def or_else(self, func, *args, **kwargs):
        if self.value is None:
            try:
                v = func(self.value, self.error, *args, **kwargs)
                return Maybe(value=v, error=None)
            except Exception as exc:
                return Maybe(value=None, error=exc)
        return self

    def ret(self, value):
        if not (self.value is None):
            try:
                return Maybe(value=value, error=None)
            except Exception as exc:
                return Maybe(value=None, error=exc)
        return self

    def value_or(self, value):
        if not (self.value is None):
            return self.value
        else:
            return value
