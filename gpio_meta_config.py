class GpioMetaConfig:
    __area_to_gpio = None
    __gpio_to_area = None

    @classmethod
    def init(cls):
        cls.__area_to_gpio = {k: v for k, v in cls.__dict__.items()
            if not k.startswith('_') and not isinstance(v, classmethod)}
        cls.__gpio_to_area = {v: k for k, v in cls.__area_to_gpio.items()}

    @classmethod
    def get_areas(cls):
        return list(cls.__area_to_gpio.keys())

    @classmethod
    def get_gpios(cls):
        return list(cls.__gpio_to_area.keys())

    @classmethod
    def area_to_gpio(cls, area):
        return cls.__area_to_gpio[area]

    @classmethod
    def gpio_to_area(cls, gpio):
        return cls.__gpio_to_area[gpio]
