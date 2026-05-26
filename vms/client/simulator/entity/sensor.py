import random
import math

# Дата рождения: 15.10.2002
BIRTH_DAY = 15
BIRTH_MONTH = 10
BIRTH_YEAR = 2002


class Sensor:
    value: float
    name: str
    type: str

    def __init__(self, name: str):
        self.name = name

    def generate_new_value(self):
        pass

    def get_data(self) -> float:
        return self.value


class Temperature(Sensor):
    _step = 0

    def __init__(self, name):
        super().__init__(name)
        self.type = "temperature"

    def generate_new_value(self):
        amplitude = BIRTH_DAY / 3
        self.value = round(25.0 + amplitude * math.sin(self._step * 0.1) + random.uniform(-0.5, 0.5), 2)
        Temperature._step += 1


class Pressure(Sensor):
    def __init__(self, name):
        super().__init__(name)
        self.type = "pressure"

    def generate_new_value(self):
        offset = BIRTH_MONTH / 10
        self.value = round(760.0 + offset * random.uniform(-10, 10), 2)


class Current(Sensor):
    _step = 0

    def __init__(self, name):
        super().__init__(name)
        self.type = "current"

    def generate_new_value(self):
        scale = (BIRTH_YEAR % 100) * 0.005
        self.value = round(abs(math.sin(Current._step * 0.2)) * scale + random.uniform(0, 0.1), 3)
        Current._step += 1


class Humidity(Sensor):
    def __init__(self, name):
        super().__init__(name)
        self.type = "humidity"
        self.value = 60.0

    def generate_new_value(self):
        step = BIRTH_DAY / 15
        self.value = round(max(30.0, min(90.0, self.value + random.uniform(-step, step))), 2)
