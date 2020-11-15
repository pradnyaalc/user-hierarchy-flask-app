from CollectionInterface import Collection
from models import Role

class RolesCollection(Collection):
    roles_collection = dict()
    root = None

    def read_data_and_build_hierarchy(self, collection, schema_path):
        """
        Reads the given roles json and creates a role dictionary collection
        :param collection: roles data list
        :param schema_path: schema to validate the input data
        :return:
        """
        # validate the given input against given schema
        if self.validate_collection(collection, schema_path):
            for role in collection:
                role_obj = Role(role['Id'], role['Name'], role['Parent'])
                self.roles_collection[role_obj.id] = role_obj
                # set root of the role hierarchy
                if role_obj.parent == 0:
                    self.root = role_obj
        else:
            raise Exception("Error in the given json file")

    def get_subordinates(self, parent_role):
        """
        Get all the subordinates and the subordinate's subordinates of the given parent role
        :param parent_role: Parent role object
        :return:
        """
        role = parent_role
        #check if given parent_role exists in created roles collection
        if role.id in self.roles_collection and role in self.roles_collection.values():
            subs = self.get_subordinate_by_id(role.id)
            role.subordinates = subs
            if len(subs) == 0:
                return
            for rol in subs:
                self.get_subordinates(rol)
        else:
            raise Exception("Parent node does not exists in the given json data")

    def get_subordinate_by_id(self, id):
        """
        Get immediate subordinates given the parent role id
        :param id: parent role id
        :return: immediate subordinate role objects
        """
        subordinates = []
        for role in self.roles_collection.values():
            if role.parent == id:
                subordinates.append(role)
        return subordinates

    def get_roles_collection(self):
        """
        :return: roles dictionary collection
        """
        return self.roles_collection

    def get_root_role(self):
        return self.root