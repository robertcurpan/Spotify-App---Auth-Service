from spyne import ComplexModel, String, Array, Integer


class UserAndRoles(ComplexModel):
    # Trebuie neaparat sa specific ce tip de date Spyne sunt campurile (altfel, spyne vede obiectul ca fiind empty)
    # Spyne se uita doar la datele care au tip de date particular bibliotecii.
    userId = Integer
    username = String
    roles = Array(String, wrapped=False)

    def __init__(self, userId, username, role_list):
        super(UserAndRoles, self).__init__()
        self.userId = userId
        self.username = username
        self.roles = role_list

