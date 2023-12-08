# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

class Registry(object):
    registry = {}

    @classmethod
    def register(cls, item):

        def decorator(item_class):
            if cls.__name__ not in cls.registry:
                cls.registry[cls.__name__] = {}

            cls.registry[cls.__name__][item] = item_class
            return item_class

        return decorator

    @classmethod
    def keys(cls):
        return cls.registry[cls.__name__].keys()

    @classmethod
    def get(cls, item):
        current_registry = cls.registry[cls.__name__]
        if item not in current_registry:
            raise Exception(f'{item} is not registered yet.\nRegistered keys: {", ".join(current_registry.keys())}')

        return current_registry[item]

class ReducerRegistry(Registry):
    pass

