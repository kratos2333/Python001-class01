from abc import ABCMeta

'''
具体要求：
if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')

定义“动物”、“猫”、“动物园”三个类，动物类不允许被实例化。
动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，猫类继承自动物类。
动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
'''


class Animal(metaclass=ABCMeta):
    def __init__(self, type, size, character):
        self._type = type
        self._size = size
        self._character = character
        # “体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
        self._is_fierce_animal = (self._size in ('中等', '大')) and self._type == '食肉' and self._character == '凶猛'


class Cat(Animal):

    def __init__(self, name, type, size, character):
        super().__init__(type, size, character)
        self._name = name

    @classmethod
    def sound(cls):
        print("Meow")

    # if not fierce_animal, then ok to be pet
    def suitable_as_pet(self):
        return not self._is_fierce_animal


class Zoo(object):
    def __init__(self, name):
        self._name = name
        self._animals = {}

    # “添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
    def add_animal(self, animal):
        if isinstance(animal, Cat):
            if 'Cat' not in self._animals.keys():
                animal_set = set()
                animal_set.add(animal)
                self._animals['Cat'] = animal_set
            else:
                animal_set = self._animals['Cat']
                animal_set.add(animal)

    def Cat(self):
        return 'Cat' in self._animals.keys()
