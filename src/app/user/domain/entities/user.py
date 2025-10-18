class User:
    def __init__(self, id: int | None, name: str, email: str, hashed_password: str):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password

    def can_login(self) -> bool:
        return bool(self.email and self.hashed_password)
