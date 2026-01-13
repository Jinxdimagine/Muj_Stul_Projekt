from Entity.ShiftType import ShiftType
class Shift_typeController:
    def __init__(self, shift_type_dao):
        self.dao = shift_type_dao

    def get_all(self):
        rows=self.dao.get_all()
        shifts_type=[]
        for s in rows:
            shift_type=ShiftType(shift_type_id=s['id'],name=s['name'])
            shifts_type.append(shift_type)
        return shifts_type# vrací list Position entity

    def get_id_by_name(self, name):
        return self.dao.get_id_by_name(name)
