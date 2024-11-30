import os
import pyautogui as pg

# Получаем масштабный коэффициент экрана, который нужен для корректной работы с pyautogui
# Это необходимо для корректной работы с различными разрешениями экрана и пиксельными точностями
pixelRatio = pg.screenshot().size[0] / pg.size().width
print(f"Pixel Ratio: {pixelRatio}")  # Выводим масштабный коэффициент для отладки


def open_calculator():
    """Функция для открытия калькулятора в зависимости от операционной системы."""
    system = os.name  # Определяем операционную систему
    if system == "nt":  # Windows
        os.system("start calc")  # Открываем калькулятор на Windows
    elif system == "posix":  # Для macOS или Linux
        if os.uname().sysname == "Darwin":  # macOS
            os.system("open -a Calculator")  # Открываем калькулятор на macOS
        else:  # Linux
            os.system("gnome-calculator")  # Открываем калькулятор на Linux
    else:
        raise OSError("Unsupported operating system")  # Если система не поддерживается, выбрасываем исключение
    pg.sleep(2)  # Подождем 2 секунды, чтобы калькулятор успел загрузиться


def click_button(image):
    """Функция для поиска и клика по кнопке калькулятора по изображению."""
    # Ищем на экране изображение кнопки (например, "1.png", "2.png", и т.д.)
    location = pg.locateOnScreen(image)

    if location:  # Если кнопка найдена на экране
        # Повторно ищем кнопку с улучшенной точностью (с параметром confidence=0.9)
        location = pg.locateOnScreen(image, confidence=0.9)
        print(f"Кнопка {image} найдена на координатах: {location}")  # Выводим местоположение кнопки для отладки

        # Находим центр кнопки для клика
        location_point = pg.center(location)
        location_x, location_y = location_point

        # Выполняем клик, корректируя координаты с учетом масштабного коэффициента
        pg.click(location_x / pixelRatio, location_y / pixelRatio)
        pg.sleep(0.1)  # Добавляем небольшую задержку между кликами
        print(f"Кнопка {image} нажата")  # Выводим сообщение о том, что кнопка была нажата
    else:
        # Если кнопка не найдена, делаем скриншот для анализа проблемы
        screenshot = pg.screenshot()
        screenshot.save("error_screenshot.png")
        raise ValueError(f"Кнопка {image} не найдена на экране.")  # Выбрасываем исключение, если кнопка не найдена


def perform_calculation():
    """Функция для выполнения сложения 12 + 7."""
    # Список изображений кнопок для ввода 12 + 7 и нажатия "="
    buttons = ["1.png", "2.png", "+.png", "7.png", "=.png"]

    # Проходим по всем кнопкам и выполняем клик
    for button in buttons:
        click_button(button)


# Основная часть программы, которая запускает все действия
if __name__ == '__main__':
    open_calculator()  # Открываем калькулятор
    perform_calculation()  # Выполняем вычисление 12 + 7