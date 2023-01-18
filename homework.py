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
        """Рассчитывает дистанцию в км.

        Returns:
            Возвращает дистанцию в км.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю скорость движения в км/ч.

        Returns:
            Возвращает среднюю скорость движения в км/ч.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий.

        Returns:
            Возвращает количество затраченных калорий
            за тренировку в ккал.
        Raises:
            NotImplementedError: исключение вызывается,
            если метод get_spent_calories()
            не будет определен в дочерних классах.
        """
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение
        о выполненной тренировке.
        """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий.

        Returns:
            Возвращает количество затраченных калорий
            за тренировку (Running) в ккал.
        """
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
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
    KMH_IN_MSEC = 0.278  # 1000 (м в км) / 3600 (сек в ч)
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
        """Рассчитывает количество затраченных калорий.

        Returns:
            Возвращает количество затраченных калорий
            за тренировку (SportsWalking) в ккал.
        """
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + (
                ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2)
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
        """Рассчитывает проплытую дистанцию в км.

        Returns:
            Возвращает проплытую дистанцию за тренировку в км.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю скорость движения в км/ч.

        Returns:
            Возвращает среднюю скорость движения
            за тренировку (Swimming) в км/ч.
        """
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий.

        Returns:
            Возвращает количество затраченных калорий
            за тренировку (Swimming) в ккал.
        """
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


def main(training: Training) -> None:
    """Главная функция.

    Args:
        training - объект дочерних классов.
    """
    print(training.show_training_info().get_message())


TRANING_CLASSES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[float]) -> Training:
    """Считывает данные полученные от датчиков.

    Args:
        workout_type - вид тренировки.
        data - показатели тренировки.
    """
    try:
        return TRANING_CLASSES[workout_type](*data)
    except (TypeError, KeyError) as err:
        raise SystemExit(
            f'Ошибка: {type(err).__name__}. '
            f'Комментарий: введены не верные данные. '
            f'Тип тренировки: {workout_type}. '
        )


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            main(read_package(workout_type, data))
        except NotImplementedError:
            raise SystemExit(
                f'Метод get_spent_calories() в классе '
                f'{TRANING_CLASSES[workout_type].__name__} не определен'
            )
