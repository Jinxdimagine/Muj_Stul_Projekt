# Controller/PositionController.py
class PositionController:
    def __init__(self, position_dao):
        self.dao = position_dao

    def get_all(self):
        list=self.dao.get_all()
        return list# vrací list Position entity

    def get_id_by_name(self, name):
        return self.dao.get_id_by_name(name)
