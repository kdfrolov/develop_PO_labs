import threading
import random
import time

class Flower:
    def __init__(self, id):
        self.id = id
        self.is_wilted = False
        self.lock = threading.Lock()

    def wilt(self):
        with self.lock:
            self.is_wilted = True

    def water(self, id_gardener):
        with self.lock:
            if self.is_wilted:
                self.is_wilted = False
                print(f"Gardener {id_gardener} watered flower {self.id}")


class Gardener:
    def __init__(self, id, flowers):
        self.id = id
        self.flowers = flowers

    def work(self):
        while True:
            wilted_flowers = [f for f in self.flowers if f.is_wilted]
            if wilted_flowers:
                flower_to_water = random.choice(wilted_flowers)  # Выбираем случайный увядший цветок
                flower_to_water.water(self.id)
            time.sleep(random.uniform(0.5, 2)) # Садовник работает с перерывами


def main(num_flowers, num_gardeners):
    flowers = [Flower(i) for i in range(num_flowers)]
    gardeners = [Gardener(i, flowers) for i in range(num_gardeners)]

    threads = []
    for gardener in gardeners:
        thread = threading.Thread(target=gardener.work)
        threads.append(thread)
        thread.start()

    # Симуляция увядания цветов (можно сделать более сложной)
    n = 0
    while True:
        print(f"Iteration {n}")
        n += 1
        for flower in flowers:
            if random.random() < 0.1: # 10% шанс увядания за итерацию
                flower.wilt()
        time.sleep(1)


if __name__ == "__main__":
    num_flowers = 10
    num_gardeners = 3
    main(num_flowers, num_gardeners)
