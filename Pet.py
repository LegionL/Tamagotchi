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

        self.health = 10
        self.max_health = 100
        self.health_updated_time = t0

        self.food = 5
        self.max_food = 10
        self.food_updated_time = t0

        self.water = 5
        self.max_water = 10
        self.water_updated_time = t0

        self.energy = 5
        self.max_energy = 10
        self.energy_updated_time = t0

        self.location = None
        self.state = State.AWAKE

        self.stage = None
        self.poop_updated_time = t0

    def gain_age(self, diff=1):
        self.age = self.age + int(diff)
        self.age = max(0, self.age)
        self.age_updated_time = time.time()

    def eat(self, diff=1):
        if diff < 0 or self.state == State.AWAKE:
            self.food = self.food + int(diff)
            self.food = max(0, min(self.food, self.max_food))
            self.food_updated_time = time.time()
            if diff > 0:
                self.stage.add_notifications(
                    '[Eat]     Cat eats some catfood')
        else:
            self.stage.add_notifications(
                '[Eat]     Failed. Cat is sleeping')

    def drink(self, diff=1):
        if diff < 0 or self.state == State.AWAKE:
            self.water = self.water + int(diff)
            self.water = max(0, min(self.water, self.max_water))
            self.water_updated_time = time.time()
            if diff > 0:
                self.stage.add_notifications(
                    '[Drink]   Cat drinks some water')
        else:
            self.stage.add_notifications(
                '[Drink]   Failed. Cat is sleeping')

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
            self.stage.add_notifications('[Dead]   Cat dies')
            return -1

        t0 = time.time()

        # age
        diff, _ = divmod(t0 - self.age_updated_time, 60)
        if diff != 0:
            self.gain_age(diff)

        # starve
        diff, _ = divmod(t0 - self.food_updated_time, 10)
        if diff != 0:
            self.eat(-diff)

        # thirst
        diff, _ = divmod(t0 - self.water_updated_time, 20)
        if diff != 0:
            self.drink(-diff)

        # lose/gain energy
        if self.state != State.SLEEP:
            diff, _ = divmod(t0 - self.energy_updated_time, 5)
            if diff != 0:
                self.gain_energy(-diff)
        else:
            diff, _ = divmod(t0 - self.energy_updated_time, 3)
            if diff != 0:
                self.gain_energy(diff)

        diff, _ = divmod(t0 - self.poop_updated_time, 20)
        if diff != 0:
            self.poop()

        diff, _ = divmod(t0 - self.health_updated_time, 20)
        if diff != 0:
            if self.food >= 5 or self.water >= 5:
                self.gain_health(diff)
            else:
                self.gain_health(-diff)

        if self.health <= 0 or self.age >= 20:
            self.die()
        if self.energy <= 4:
            self.sleep()
        elif self.energy >= 8:
            self.wake_up()

    def die(self, ):
        self.state = State.DEAD

    def poop(self, forced=False):
        if self.state == State.AWAKE:
            self.stage.items.append('poop')
            if forced:
                self.stage.add_notifications(
                    '[Poop]    the Cat poops RELUCTANTLY.')
            else:
                self.stage.add_notifications(
                    '[Poop]    the Cat poops.')
        else:
            self.stage.add_notifications(
                '[Poop]    Failed. the Cat is sleeping.')
        self.poop_updated_time = time.time()

    def sleep(self, ):
        if self.state != State.SLEEP:
            self.state = State.SLEEP
            self.stage.add_notifications('[Sleep]   Cat sleeps.')

    def wake_up(self, ):
        if self.state != State.AWAKE:
            self.state = State.AWAKE
            self.stage.add_notifications('[Wake up] Cat wakes up.')

    def __str__(self, ):
        return f'Cat State: {self.state.name}  Age: {self.age}  '\
               f'Health: {self.health}  '\
               f'Food: {self.food}  Water: {self.water}  Energy: {self.energy}'
