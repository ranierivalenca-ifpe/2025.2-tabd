from faker import Faker


class FakerUniqueWithin(Faker):
    def __init__(self, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def unique_except(self, used_set):
        # check if used_set is a set
        if not isinstance(used_set, set):
            if isinstance(used_set, list):
                used_set = set(used_set)
            else:
                raise ValueError("used_set must be a set or a list")

        class UniqueProxy(Faker):
            def __init__(self, faker_instance, used):
                self.faker_instance = faker_instance
                self.used = used

            def __getattr__(self, name):
                attr = getattr(self.faker_instance, name)
                if callable(attr):

                    def wrapper(*args, **kwargs):
                        for _ in range(100):  # Avoid infinite loops
                            value = attr(*args, **kwargs)
                            if value not in self.used:
                                self.used.add(value)
                                return value
                        raise ValueError(
                            "Could not generate a unique value after 100 attempts"
                        )

                    return wrapper
                return attr

        return UniqueProxy(self, used_set)

    def from_list(self, lst):
        return self.random_choices(lst, length=1)[0]


# Example usage:
# fake = FakerUniqueWithin()
# used_emails = set()
# unique_email = fake.unique_with(used_emails).email()
