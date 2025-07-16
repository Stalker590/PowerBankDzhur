class PowerBank:
    def __init__(self, name, price, capacity, number):
        self.name = name
        self.price = price
        self.capacity = capacity
        self.number = number

# Створення об'єктів
power1 = PowerBank("PowerBank 1", 100, 1000, 0)
power2 = PowerBank("PowerBank 2", 150, 1500, 1)
power3 = PowerBank("PowerBank 3", 200, 2000, 2)

# Список усіх
power_banks = [power1, power2, power3]

# Вивід
for power_bank in power_banks:
    print(power_bank)
