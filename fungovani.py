
from databaze import Databaze


class Fungovani:
    def __init__(self, on_login_success=None):
        self.db = Databaze()
        self.prihlaseny_uzivatel = None
        self.on_login_success = on_login_success

    def register(self, username, password):
        return self.db.vytvor_ucet(username, password)

    def login(self, username, password):
        if not username.strip() or not password:
            return False, "Please fill in all fields."

        user = self.db.over_ucet(username, password)

        if user is None:
            return False, "Invalid username or password."

        self.prihlaseny_uzivatel = user

        if self.on_login_success:
            self.on_login_success(user["username"])

        return True, "Login successful!"

    def logout(self):
        self.prihlaseny_uzivatel = None

    def delete_account(self):
        if self.prihlaseny_uzivatel is None:
            return False, "No user is logged in."

        user_id = self.prihlaseny_uzivatel["id"]
        deleted = self.db.smaz_uzivatele(user_id)

        if deleted:
            self.prihlaseny_uzivatel = None
            return True, "Account deleted successfully."

        return False, "Could not delete the account."

    def get_dogs(self):
        return self.db.seznam_psu()

    def add_dog(
        self,
        name,
        breed="",
        age=None,
        description="",
        image_path=None
    ):
        return self.db.pridej_psa(
            name, breed, age, description, image_path
        )
