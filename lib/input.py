import survey


class Input:
    basic_input = survey.routines.input

    def select(*args, **kwargs):
        return survey.routines.select(*args, **kwargs, permit=True, clean=False)

    @staticmethod
    def spin(msg_while, msg_done, func=lambda self: None, *args, **kwargs):
        return survey.graphics.SpinProgress(
            prefix=msg_while,
            suffix=func,
            epilogue=msg_done,
            *args,
            **kwargs
        )
