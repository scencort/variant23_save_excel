import pandas as pd
from datetime import date

"""Класс товара"""
class Product:
    def __init__(self, name, proizvoditel, price):
        self.name = name
        self.proizvoditel = proizvoditel
        self.price = price

"""Класс клиента"""
class Client:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

"""Класс ремонта"""
class Repair:
    def __init__(self, product):
        self.product = product

    def get_cost(self):
        return 0 #по дефолту ничего не стоит

"""Замена товара (стоимость равна цене товара)"""
class Repl_repair(Repair):
    def get_cost(self):
        return self.product.price

"""Ремонт товара (у меня по заданию фиксированная цена)"""
class FixRepair(Repair):
    def get_cost(self):
        return 50 #вот как раз эта цена

"""Метод для создания объектов ремонта"""
class RepairFactory:
    @staticmethod
    def create_repair(type, product):
        if type == "замена":
            return Repl_repair(product)
        elif type == "ремонт":
            return FixRepair(product)
        else:
            raise ValueError("Нет такого типа ремонта")
        
"""Класс заявки по гарантии"""
class Warranty:
    def __init__(self, product, client, date):
        self.product = product
        self.client = client
        self.date = date
        self.status = "Новая"
        self.repair = None

"""Секретарь у меня принимает заявку на товар"""
class Secretary:
    def accept_request(self, request):
        request.status = "Принята"
        print(f"Приемщик принял заявку на товар: {request.product.name}")

"""Мастер проверяет товары у меня"""
class Technician:
    def analyze_product(self, request):
        request.status = "Проверена"
        print(f"Мастер проверил товар: {request.product.name}")

"""Менеджер"""
class Manager:
    def decide_action(self, request, type):
        request.repair = RepairFactory.create_repair(type, request.product)
        request.status = "Готово"
        print(f"Менеджер решил: {request.product.name} — {type}")


"""Создаю товары и клиента"""
p1 = Product("Жесткий диск", "Seagate", 120)
p2 = Product("Оперативная память", "Kingston", 80)
client = Client("Иван Петров", "ivan@mail.com")

"""Создаю заявки"""
requests = [
    Warranty(p1, client, date(2025, 11, 5)),
    Warranty(p2, client, date(2025, 11, 5))
]

"""Создаю работников"""
secretary = Secretary()
technician = Technician()
manager = Manager()

"""Обработка заявок циклом"""
for req in requests:
    secretary.accept_request(req)
    technician.analyze_product(req)
    #Решений у меня даётся несколько: ремонт или замена
    if req.product.name == "Оперативная память":
        manager.decide_action(req, "ремонт")
    else:
        manager.decide_action(req, "замена")


"""Дальше у меня работа с библиотекой openpyxl"""
"""Формирую данные для отчета"""
report = []
for req in requests:
    repair_type = "Замена" if isinstance(req.repair, Repl_repair) else "Ремонт"
    report.append({
        "Товар": req.product.name,
        "Производитель": req.product.proizvoditel,
        "Тип ремонта": repair_type,
        "Стоимость": req.repair.get_cost(),
        "Клиент": req.client.name,
        "Дата": req.date
    })

"""Создаем таблицу pandas"""
df = pd.DataFrame(report)

"""Группировка по типу ремонта (итог)"""
df_sum = df.groupby("Тип ремонта")["Стоимость"].sum().reset_index()
df_sum.rename(columns={"Стоимость": "Суммарные затраты"}, inplace=True)

"""Сохранение в excel"""
with pd.ExcelWriter("отчёт.xlsx") as writer:
    df.to_excel(writer, sheet_name="Подробно", index=False)
    df_sum.to_excel(writer, sheet_name="Итоги", index=False)

print(df_sum)