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

    def _change_prior_dict(self, key):
        self.__prior_dict[key] = self.__cur_prior
        self.__cur_prior += 1

        if self.__cur_prior > self.__maxprior:
            self.__cur_prior = 0
            min_prior = min(self.__prior_dict.values())
            for cur_key in self.__prior_dict:
                self.__prior_dict[cur_key] -= min_prior

    def get(self, key):
        if key in self.local_dict:
            self._change_prior_dict(key)
            return self.local_dict[key]
        return None

    def set(self, key, value):
        if key in self.local_dict:
            self._change_prior_dict(key)
            self.local_dict[key] = value
            return

        if len(self.local_dict) == self.limit:
            min_prior = min(self.__prior_dict.values())
            for cur_key, cur_val in self.__prior_dict.items():
                if cur_val == min_prior:
                    self.__prior_dict.pop(cur_key)
                    self.local_dict.pop(cur_key, None)
                    break

        self._change_prior_dict(key)
        self.local_dict[key] = value
