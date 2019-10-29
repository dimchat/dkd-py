# -*- coding: utf-8 -*-

from mkm import *

from .immortals import *


class Facebook(UserDataSource):

    def __init__(self):
        super().__init__()
        self.__private_keys = {}
        self.__metas = {}
        self.__profiles = {}
        self.__users = {}

    def cache_private_key(self, private_key: PrivateKey, identifier: ID):
        self.__private_keys[identifier.address] = private_key

    def cache_meta(self, meta: Meta, identifier: ID):
        self.__metas[identifier.address] = meta

    def cache_profile(self, profile: Profile, identifier: ID):
        self.__profiles[identifier.address] = profile

    def cache_user(self, user: User):
        if user.delegate is None:
            user.delegate = self
        self.__users[user.identifier.address] = user

    def user(self, identifier: ID) -> User:
        user = self.__users.get(identifier.address)
        # TODO: if user not found, create one?
        return user

    #
    # Delegates
    #

    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        key = self.__private_keys.get(identifier.address)
        return key

    def private_keys_for_decryption(self, identifier: ID) -> list:
        key = self.__private_keys.get(identifier.address)
        return [key]

    def contacts(self, identifier: ID) -> list:
        # TODO: get contacts with user ID
        pass

    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        # TODO: save meta with entity ID
        pass

    def meta(self, identifier: ID) -> Meta:
        return self.__metas.get(identifier.address)

    def profile(self, identifier: ID) -> Profile:
        return self.__profiles.get(identifier.address)


facebook = Facebook()

facebook.cache_private_key(private_key=moki_sk, identifier=moki_id)
facebook.cache_private_key(private_key=hulk_sk, identifier=hulk_id)

facebook.cache_meta(meta=moki_meta, identifier=moki_id)
facebook.cache_meta(meta=hulk_meta, identifier=hulk_id)

facebook.cache_profile(profile=moki_profile, identifier=moki_id)
facebook.cache_profile(profile=hulk_profile, identifier=hulk_id)

facebook.cache_user(moki)
facebook.cache_user(hulk)
