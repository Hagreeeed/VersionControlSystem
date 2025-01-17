
class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id
    def get_repositories(self, db):
        return db.get_user_repositories(self.user_id)

class Admin(User):
    def get_repositories(self, db):
        if db.is_admin(self.username):
            return db.get_all_repositories()
