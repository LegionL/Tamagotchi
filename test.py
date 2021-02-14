import unittest
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

    def test_pet_die_of_low_health(self):
        self.pet.health = 1
        self.pet.update()
        self.assertEqual(self.pet.state, State.AWAKE)

        self.pet.health = 0
        self.pet.update()
        self.assertEqual(self.pet.state, State.DEAD)

    def test_pet_eat(self):
        prev = self.pet.food
        self.pet.eat()
        self.pet.update()
        self.assertEqual(self.pet.food, prev + 1)

    def test_pet_food_upper_limit(self):
        self.pet.food = 10
        self.pet.eat()
        self.pet.update()
        self.assertEqual(self.pet.food, 10)

    def test_pet_starve(self):
        prev = self.pet.food
        self.pet.food_updated_time = self.pet.food_updated_time - 10
        self.pet.update()
        self.assertEqual(self.pet.food, prev - 1)

    def test_pet_eat_while_sleeping(self):
        prev = self.pet.food
        self.pet.state = State.SLEEP
        self.pet.eat()
        self.pet.update()
        self.assertEqual(self.pet.food, prev)

    def test_water_upper_limit(self):
        self.pet.water = 10
        self.pet.drink()
        self.pet.update()
        self.assertEqual(self.pet.water, 10)

    def test_pet_drink(self):
        prev = self.pet.food
        self.pet.eat()
        self.pet.update()
        self.assertEqual(self.pet.food, prev + 1)

    def test_pet_thirst(self):
        prev = self.pet.water
        self.pet.water_updated_time = self.pet.water_updated_time - 20
        self.pet.update()
        self.assertEqual(self.pet.water, prev - 1)

    def test_pet_drink_while_sleeping(self):
        prev = self.pet.water
        self.pet.state = State.SLEEP
        self.pet.drink()
        self.pet.update()
        self.assertEqual(self.pet.water, prev)

    def test_energy_lost_over_time(self):
        prev = self.pet.energy
        self.pet.energy_updated_time = self.pet.water_updated_time - 10
        self.pet.update()
        self.assertEqual(self.pet.energy, prev - 1)

    def test_sleep_when_energy_is_low(self):
        self.pet.energy = 4
        self.pet.update()
        self.assertEqual(self.pet.state, State.SLEEP)

    def test_wake_up(self):
        self.pet.energy = 8
        self.pet.state = State.SLEEP
        self.pet.update()
        self.assertEqual(self.pet.state, State.AWAKE)

    def test_eneragy_regen_during_sleep(self):
        self.pet.energy = 5
        self.pet.state = State.SLEEP
        self.pet.energy_updated_time = self.pet.water_updated_time - 3
        self.pet.update()
        self.assertEqual(self.pet.energy, 6)

    def test_poop(self):
        self.assertEqual('poop' in self.stage.items, False)
        self.pet.poop_updated_time = self.pet.poop_updated_time - 20
        self.pet.update()
        self.assertEqual('poop' in self.stage.items, True)


if __name__ == '__main__':

    unittest.main()
