class Cache:
    def __init__(self):
        """Initializes new instance of the Cache class."""
        self.__cache = {}

    def set(self, oid, entity):
        """Adds object to cache
        :type oid: str
        :type entity: object
        :param oid: Object Id
        :param entity: Object"""
        self.__cache[oid] = entity

    def get(self, oid):
        """Returns cached object if any
        :param oid: Object Id
        :return: Object, None if nothing found"""
        result = self.__cache.get(oid, None)
        return result

    def remove(self, oid):
        """Removes object from cache
        :param oid: Object Id"""
        if oid in self.__cache:
            del self.__cache[oid]
