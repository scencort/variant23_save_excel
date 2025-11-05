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
report = [] #созда. пустой список, в который будe добавлять словари с данными о каждой заявке

for req in requests:
    #определя. тип ремонта по классу объекта (Repl_repair - это замена, иначе - ремонт)
    repair_type = "Замена" if isinstance(req.repair, Repl_repair) else "Ремонт"

    #добавляю словарь с нужными данными по заявке
    report.append({
        "Товар": req.product.name,                #название товара
        "Производитель": req.product.proizvoditel,#производитель
        "Тип ремонта": repair_type,               #"Замена" или "Ремонт"
        "Стоимость": req.repair.get_cost(),       #сумма ремонта или замены
        "Клиент": req.client.name,                #имя клиента
        "Дата": req.date                          #дата обращения
    })

"""Создаем таблицу pandas"""
df = pd.DataFrame(report) #создаю таблицу (DataFrame) из списка словарей report
#pandas автоматически создаёт столбцы по ключам словаря ("Товар", "Тип ремонта", "Стоимость" и т.д.)

"""Группировка по типу ремонта (итог)"""
#группирую данные по колонке "Тип ремонта" (например, "Ремонт", "Замена")
#и считаю общую сумму по колонке "Стоимость" для каждой группы
df_sum = df.groupby("Тип ремонта")["Стоимость"].sum().reset_index()

#переименовываю колонку "Стоимость" в "Суммарные затраты" - чтобы отчёт выглядел красиво
df_sum.rename(columns={"Стоимость": "Суммарные затраты"}, inplace=True)

"""Сохранение в excel"""
#создаю ExcelWriter - объект, который позволяет записывать несколько листов в один Excel-файл
with pd.ExcelWriter("отчёт.xlsx") as writer:
    #первый лист - детальная таблица с каждой заявкой
    df.to_excel(writer, sheet_name="Подробно", index=False)
    #второй лист - сгруппированные итоги по типам ремонта
    df_sum.to_excel(writer, sheet_name="Итоги", index=False)

#вывожу таблицу с итогами в консоль (для наглядности)
print(df_sum)
