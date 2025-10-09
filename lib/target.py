class Target:
    def __init__(self, name: str, func, pre=None):
        self.name = name
        self.func = func
        self.pre = pre

    def __str__(self):
        return self.name.lower()

    def __call__(self):
        args = ()
        if self.pre:
            result = self.pre()
            if result is None:
                return
            args = (result,)
        return self.func(*args)
