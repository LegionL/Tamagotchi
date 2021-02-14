from abc import ABC, abstractmethod
import time


class Pet(ABC):

    @abstractmethod
    def eat(self):
        pass


class Cat(Pet):

    def __init__(self, ):
        t0 = time.time()
        self.age = 0

        self.health = 80
        self.max_health = 100
        self.health_updated_time = t0

        self.food = 8
        self.max_food = 10
        self.food_updated_time = t0

        self.water = 8
        self.max_water = 10
        self.water_updated_time = t0

        self.energy = 8
        self.max_energy = 10
        self.energy_updated_time = t0

        self.location = None
        self.state = None

        self.stage = None

    def eat(self, diff=1):
        self.food = self.food + int(diff)
        self.food = max(0, min(self.food, self.max_food))
        self.food_updated_time = time.time()

    def drink(self, diff=1):
        self.water = self.water + int(diff)
        self.water = max(0, min(self.water, self.max_water))
        self.water_updated_time = time.time()

    def gain_energy(self, diff=1):
        self.energy = self.energy + int(diff)
        self.energy = max(0, min(self.energy, self.max_energy))
        self.energy_updated_time = time.time()

    def gain_health(self, diff=1):
        self.health = self.health + int(diff)
        self.health = max(0, min(self.health, self.max_health))
        self.health_updated_time = time.time()

    def update(self, ):
        t0 = time.time()
        sleep_modifier = 1 if self.state != 'sleep' else 3

        diff, _ = divmod(t0 - self.food_updated_time, 10 * sleep_modifier)
        self.eat(-diff)

        diff, _ = divmod(t0 - self.water_updated_time, 20 * sleep_modifier)
        self.drink(-diff)

        diff, _ = divmod(t0 - self.energy_updated_time, 30)
        self.gain_energy(-diff)

        diff, _ = divmod(t0 - self.health_updated_time, 20 * sleep_modifier)
        if self.food >= 5 or self.water >= 5:
            self.gain_health(diff)
        else:
            self.gain_health(-diff)

    def poop(self, ):
        self.stage.append('poop')

    def sleep(self, ):
        t0 = time.time()
        self.state = 'sleep'
        diff, _ = divmod(t0 - self.energy_updated_time, 10)
        self.gain_energy(diff)

    def wake_up(self, ):
        self.state = 'idle'

    def __str__(self, ):
        return f'Pet: Cat  Age: {self.age}  Food: {self.food}  '\
               f'Water: {self.water}  Energy: {self.energy}'


if __name__ == '__main__':
    c = Cat()
    c.eat()
    print(c)
    c.eat()
    print(c)
    c.eat()
    print(c)
    time.sleep(20)
    c.update()
    print(c)
