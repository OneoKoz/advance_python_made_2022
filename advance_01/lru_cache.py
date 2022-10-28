import sys

from custom_logger import logging

if "-s" in sys.argv:
    logger = logging.getLogger("main_with_stdout")
else:
    logger = logging.getLogger()


class LRUCache:
    """
    custom lru cache dict
    """

    def __init__(self, limit=42):
        """
        init method
        :param limit: max size of dict
        __prior_dict - need for save and change prior for any existed key
        __cur_prior - current prior num
        __maxprior - prior ather which all prior are recalculated
        """
        limit = max(limit, 1)
        self.limit = limit
        self.local_dict = {}
        self.__prior_dict = {}
        self.__cur_prior = 0
        self.__maxprior = 100_000 * limit
        logger.info("new dict is created with limit = %s", limit)

    def _change_prior_dict(self, key):
        logger.debug('start "%s" method with param %s', self._change_prior_dict.__qualname__, key)
        self.__prior_dict[key] = self.__cur_prior
        self.__cur_prior += 1

        if self.__cur_prior > self.__maxprior:
            logger.warning("change num of prior for all keys")
            self.__cur_prior = 0
            min_prior = min(self.__prior_dict.values())
            for cur_key in self.__prior_dict:
                self.__prior_dict[cur_key] -= min_prior

    def get(self, key):
        logger.debug('start "%s" method with param %s', self.get.__qualname__, key)
        if key in self.local_dict:
            self._change_prior_dict(key)
            logger.info('return value by key = %s', key)
            return self.local_dict[key]
        logger.warning("%s is not in dict %s", key, self.__class__.__name__)
        return None

    def set(self, key, value):
        logger.debug('start "%s" method with param %s', self.set.__qualname__, (value, key))
        if key in self.local_dict:
            self._change_prior_dict(key)
            self.local_dict[key] = value
            logger.info("changed value for existing key = %s", key)
            return

        if len(self.local_dict) == self.limit:
            logger.debug('start procedure for deleting the least priority key')
            min_prior = min(self.__prior_dict.values())
            for cur_key, cur_val in self.__prior_dict.items():
                if cur_val == min_prior:
                    self.__prior_dict.pop(cur_key)
                    logger.debug('delete key = %s', cur_key)
                    self.local_dict.pop(cur_key, None)
                    break

        self._change_prior_dict(key)
        self.local_dict[key] = value
        logger.info('new key = %s added', key)
