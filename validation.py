class Validators:
    def __init__(self):
        self.validators = []

    def add(self, validator):
        self.validators.append(validator)

    def validate(self):
        errors = set()
        for validator in self.validators:
            result = validator.func(*validator.args)

            if result is None:
                continue

            errors.add(result)

            if validator.callback is not None:
                validator.callback()

            if validator.pass_through:
                continue

        return errors

class Validator:
    def __init__(self, func, pass_through = False, callback = None, *args):
        self.func = func
        self.pass_through = pass_through
        self.callback = callback
        self.args = args

    def set_args(self, *args):
        self.args = args