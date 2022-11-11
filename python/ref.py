import yaml
import os


class Ref(yaml.YAMLObject):
    yaml_tag = u'!!python/object:ref.Ref'

    def __init__(self, id):
        self.id = id

    """
    @classmethod
    def to_yaml(cls, dumper, data):
        dict_representation = {
            'id': data.id
        }
        node = dumper.represent_mapping(Ref.yaml_tag, dict_representation)
        return node

    @classmethod
    def from_yaml(cls, loader, node):
        dict_representation = loader.construct_mapping(node)
        id = dict_representation['id']
        return load(id)
    """

    def save(self):
        with open(f"/home/agi/code/ztrezor/db/{self.id}.yaml", "w") as f:
            f.write(yaml.dump(self.i))

    def __repr__(self):
        return f"<Ref to {self.id}>"

    @staticmethod
    def new(id, obj):
        LOADED[id] = obj
        ref = Ref(id)
        ref.save()
        return ref

    @property
    def i(self):
        return LOADED[self.id]


def new(id, obj):
    assert id not in LOADED
    LOADED[id] = obj
    return Ref(id)


LOADED = dict()
for id_file in os.listdir("/home/agi/code/ztrezor/db"):
    id = id_file.split(".")[0]
    with open(f"/home/agi/code/ztrezor/db/{id}.yaml") as f:
        LOADED[id] = yaml.load(f.read(), yaml.Loader)


def get_every(cls):
    for k, v in LOADED.items():
        if isinstance(v, cls):
            yield Ref(k)
