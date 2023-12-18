class MyEnv:
    @classmethod
    def set(cls, key, value):
        setattr(cls, key, value)

    @classmethod
    def get(cls, key, default=None):
        return getattr(cls, key, default)

    @classmethod
    def dict(cls) -> dict:
        return {key: getattr(cls, key) for key in dir(cls) if not key.startswith("__") and not callable(getattr(cls, key, None))}

    @classmethod
    def update(cls, dicts: dict):
        for key, value in dicts.items():
            setattr(cls, key, value)

    @classmethod
    def items(cls) -> list:
        return [(key, getattr(cls, key)) for key in dir(cls) if not key.startswith("__") and not callable(getattr(cls, key, None))]

    @classmethod
    def keys(cls) -> list:
        return [key for key in dir(cls) if not key.startswith("__") and not callable(getattr(cls, key, None))]

    @classmethod
    def values(cls) -> list:
        return [getattr(cls, key) for key in dir(cls) if not key.startswith("__") and not callable(getattr(cls, key, None))]

    @classmethod
    def pop(cls, key, default=None):
        value = getattr(cls, key, default)
        delattr(cls, key)
        return value

    @classmethod
    def clear(cls):
        for key in list(dir(cls)):
            if not key.startswith("__") and not callable(getattr(cls, key, None)):
                delattr(cls, key)

    @classmethod
    def copy(cls) -> dict:
        return {key: getattr(cls, key) for key in dir(cls) if not key.startswith("__") and not callable(getattr(cls, key, None))}

    @classmethod
    def fromkeys(cls, keys, value=None):
        for key in keys:
            setattr(cls, key, value)
