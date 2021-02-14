import time
import unittest 
from unittest.mock import patch
from Pet import Cat, State
from Tamagotchi import Stage


class TestSum(unittest.TestCase):

    def setUp(self):
        self.pet = Cat()
        self.stage = Stage()
        self.stage.items.append(self.pet)
        self.pet.stage = self.stage

    def test_pet_age_after_time_pass(self):
        self.pet.age_updated_time = self.pet.age_updated_time - 60
        self.pet.update()
        self.assertEqual(self.pet.age, 1)

        self.pet.age_updated_time = self.pet.age_updated_time - 60
        self.pet.update()
        self.assertEqual(self.pet.age, 2)

    def test_pet_die_of_age(self):
        self.pet.age = 19
        self.pet.update()
        self.assertEqual(self.pet.age, 19)
        self.assertEqual(self.pet.state, State.AWAKE)

        self.pet.age = 20
        self.pet.update()
        self.assertEqual(self.pet.age, 20)
        self.assertEqual(self.pet.state, State.DEAD)

    def test_pet_die_of_health(self):
        self.pet.health = 1
        self.pet.update()
        self.assertEqual(self.pet.state, State.AWAKE)

        self.pet.health = 0
        self.pet.update()
        self.assertEqual(self.pet.state, State.DEAD)






if __name__ == '__main__':


    unittest.main()
