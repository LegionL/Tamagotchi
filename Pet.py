from abc import ABC, abstractmethod
import time
from enum import Enum


class State(Enum):
    SLEEP = 1
    AWAKE = 2
    DEAD = 3


class Pet(ABC):
    @abstractmethod
    def eat(self):
        pass

    @abstractmethod
    def drink(self):
        pass

    @abstractmethod
    def gain_energy(self):
        pass

    @abstractmethod
    def gain_health(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Cat(Pet):
    def __init__(self, ):
        t0 = time.time()
        self.age = 0
        self.age_updated_time = t0

        self.health = 1
        self.max_health = 100
        self.health_updated_time = t0

        self.food = 5
        self.max_food = 10
        self.food_updated_time = t0

        self.water = 5
        self.max_water = 10
        self.water_updated_time = t0

        self.energy = 8
        self.max_energy = 10
        self.energy_updated_time = t0

        self.location = None
        self.state = State.AWAKE

        self.stage = None
        self.poop_sensor = False
        self.poop_updated_time = t0

    def gain_age(self, diff=1):
        self.age = self.age + int(diff)
        self.age = max(0, self.age)
        self.age_updated_time = time.time()

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
        if self.state == State.DEAD:
            self.stage.add_notifications(f'[Dead]   the {self.__class__.__name__} dies.')
            return -1 

        t0 = time.time()
        sleep_modifier = 1 if self.state != State.SLEEP else 3
        self.poop_sensor = 'poop' in self.stage.items
        poop_modifier = 1 if self.poop_sensor == False else 0.1

        diff, _ = divmod(t0 - self.age_updated_time, 60)
        if diff != 0:
            self.gain_age(diff)

        diff, _ = divmod(t0 - self.food_updated_time, 10 * sleep_modifier)
        if diff != 0:
            self.eat(-diff)

        diff, _ = divmod(t0 - self.water_updated_time, 20 * sleep_modifier)
        if diff != 0:
            self.drink(-diff)

        diff, _ = divmod(t0 - self.energy_updated_time, 20)
        if diff != 0:
            self.gain_energy(-diff)

        diff, _ = divmod(t0 - self.poop_updated_time, 20)
        if diff != 0:
            self.poop()

        diff, _ = divmod(t0 - self.health_updated_time, 20 * sleep_modifier)
        if diff != 0:
            if self.food >= 5 or self.water >= 5:
                self.gain_health(diff)
            else:
                self.gain_health(-diff)

        if self.health <= 0 or self.age >= 20:
            self.die()

    def die(self, ):
        self.state = State.DEAD

    def poop(self, forced=False):
        self.stage.items.append('poop')
        if forced:
            self.stage.add_notifications(f'[Poop]   the {self.__class__.__name__} poops RELUCTANTLY.')
        else:
            self.stage.add_notifications(f'[Poop]   the {self.__class__.__name__} poops.')
        self.poop_updated_time = time.time()

    def sleep(self, ):
        t0 = time.time()
        self.state = State.SLEEP
        diff, _ = divmod(t0 - self.energy_updated_time, 10)
        self.gain_energy(diff)

    def wake_up(self, ):
        self.state = State.AWAKE

    def __str__(self, ):
        return f'Cat  State: {self.state.name}  Age: {self.age}  Health: {self.health}  '\
               f'Food: {self.food}  Water: {self.water}  Energy: {self.energy}'

