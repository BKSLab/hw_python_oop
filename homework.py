class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        speed = distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        message = (InfoMessage(self.__class__.__name__,
                               self.duration, distance,
                               speed, spent_calories))
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        speed_running = super().get_mean_speed()
        spent_calories_running = (((
            self.CALORIES_MEAN_SPEED_MULTIPLIER * speed_running
            + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
            / super().M_IN_KM * (self.duration * super().MIN_IN_H)))

        return spent_calories_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        speed_sports_walking = super().get_mean_speed()
        spent_calories_sports_walking = ((
            self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            + (((speed_sports_walking * self.KMH_IN_MSEC) ** 2)
                / (self.height / self.CM_IN_M))
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
            * (self.duration * super().MIN_IN_H))

        return spent_calories_sports_walking


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / super().M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_swimming = (self.length_pool
                          * self.count_pool / super().M_IN_KM / self.duration)
        return speed_swimming

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_swimming = self.get_mean_speed()
        spent_calories_swimming = ((speed_swimming
                                   + self.CALORIES_MEAN_SPEED_SHIFT)
                                   * self.CALORIES_WEIGHT_MULTIPLIER
                                   * self.weight * self.duration)
        return spent_calories_swimming


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные  полученные от датчиков."""

    training_classes: dict[str, object] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_classes[workout_type](*data)


if __name__ == '__main__':
    packages: list[str, tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
