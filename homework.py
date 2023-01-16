from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Рассчитывает дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю скорость движения."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()

        return InfoMessage(
            type(self).__name__,
            self.duration,
            distance,
            speed,
            spent_calories,
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий."""
        speed_running = self.get_mean_speed()

        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * speed_running
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278  # 1000 (м в км) / 3600 (сек. в ч.)
    CM_IN_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:

        super().__init__(
            action,
            duration,
            weight,
        )
        self.height = height

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий."""
        speed_sports_walking = self.get_mean_speed()

        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + (
                ((speed_sports_walking * self.KMH_IN_MSEC) ** 2)
                / (self.height / self.CM_IN_M)
            )
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight
        ) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:

        super().__init__(
            action,
            duration,
            weight,
        )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Рассчитывает дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий."""
        speed_swimming = self.get_mean_speed()

        return (
            (speed_swimming + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


def main(training: Training) -> None:
    """Главная функция.
    Args: training - объект дочерних классов.
    """
    print(training.show_training_info().get_message())


TRANING_CLASSES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[str]) -> Training:
    """Считывает данные полученные от датчиков.
    Args:
        workout_type - вид тренировки.
        data - показатели тренировки.
    """
    return TRANING_CLASSES[workout_type](*data)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    try:
        for workout_type, data in packages:
            main(read_package(workout_type, data))
    except TypeError:
        print(
            f'Неверное количество показателей '
            f'в тренеровке: {TRANING_CLASSES[workout_type].__name__}. '
        )
    except KeyError:
        print(f'{workout_type} - неизвестная тренеровка')
    except NotImplementedError:
        print(
            f'В классе {TRANING_CLASSES[workout_type].__name__} '
            f'Метод get_spent_calories() не определен'
        )
