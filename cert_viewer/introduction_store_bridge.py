class IntroStore(object):
    def __init__(self, intro_db):
        self.intro_db = intro_db

    def insert(self, intro):
        self.intro_db.introductions.insert_one(intro)


def insert_introduction(introduction):
    from cert_viewer import intro_store
    intro_store.insert(introduction)
