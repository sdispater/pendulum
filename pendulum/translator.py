# -*- coding: utf-8 -*-

import os
from python_translate.translations import Translator as BaseTranslator, MessageCatalogue
from python_translate.loaders import DictLoader, NotFoundResourceException

from ._compat import load_module


class Translator(BaseTranslator):

    def __init__(self, locale):
        super(Translator, self).__init__(locale)

        self.add_loader('dict', DictLoader())

    def _do_load_catalogue(self, locale):
        self.catalogues[locale] = MessageCatalogue(locale)
        if locale in self.resources:
            for resource in self.resources[locale]:
                if resource[0] not in self.loaders:
                    raise RuntimeError(
                        'The "{0}" translation loader is not '
                        'registered'.format(resource[0])
                    )
                self.catalogues[locale].add_catalogue(
                    self.loaders[resource[0]].load(
                        resource[1],
                        locale,
                        resource[2]
                    )
                )
        else:
            if not self.register_resource(locale):
                raise NotFoundResourceException('Resource for locale "%s" could not be found' % locale)

            self._do_load_catalogue(locale)

    def register_resource(self, locale):
        root_path = os.path.join(os.path.dirname(__file__), 'lang')
        root = os.path.join(root_path, '__init__.py')
        locale_file = os.path.join(root_path, '%s.py' % locale)

        if not os.path.exists(locale_file):
            return False

        # Loading parent module
        load_module('lang', root)

        # Loading locale
        locale_mod = load_module('lang.%s' % locale, locale_file)

        self.add_resource('dict', locale_mod.translations, locale)

        return True
