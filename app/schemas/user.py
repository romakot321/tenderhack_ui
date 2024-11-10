from pydantic import BaseModel


class CheckCriteriaSchema(BaseModel):
    name: bool = True
    executor: bool = True
    license: bool = True
    delivery_schedule: bool = True
    max_cost: bool = True
    start_cost: bool = True
    task_document: bool = True

    def translated_dict(self):
        return {
            "Совпадение названий": self.name,
            "Обеспечение исполнения контракта": self.executor,
            "Наличие сертификатов": self.license,
            "Соответствие графика/этапа поставки": self.delivery_schedule,
            "Соответствие максимальной цены": self.max_cost,
            "Наличие стартовой цены": self.start_cost,
            "Проверка тех. задания(товары)": self.task_document
        }


class UserSchema(BaseModel):
    telegram_id: int 
    criteria: CheckCriteriaSchema

