
# -*- encoding: utf-8 -*-

import conf

class IndexDBRouter(object):
    HOTDB = conf.DB_NAME_DEFAULT
    LEAGUEDB = conf.DB_NAME_LEAGUE
    WIKIDB = conf.DB_NAME_WIKI

    LEAGUEAPP = conf.APP_NAME_LEAGUE
    WIKIAPP = conf.APP_NAME_WIKI
    HOTAPP = conf.APP_NAME_HOT

    def allow_syncdb(self, db, model):
        if db == IndexDBRouter.LEAGUEDB or db == IndexDBRouter.WIKIDB:
            return False
        if db == IndexDBRouter.HOTDB:
            if model._meta.app_label==IndexDBRouter.HOTAPP:
                return True
            return not (model._meta.app_label == IndexDBRouter.LEAGUEAPP or
            model._meta.app_label == IndexDBRouter.WIKIAPP )


    def db_for_write(self, model, **hints):
        if not model._meta.app_label == IndexDBRouter.HOTAPP:
            return False
        else:
            return conf.DB_NAME_DEFAULT

    def db_for_read(self, model, **hints):
        if model._meta.app_label == IndexDBRouter.WIKIAPP:
            return IndexDBRouter.WIKIDB
        elif model._meta.app_label == IndexDBRouter.LEAGUEAPP:
            return IndexDBRouter.LEAGUEDB
        elif model._meta.app_label == IndexDBRouter.HOTAPP:
            return IndexDBRouter.HOTDB
        else:
            return None






