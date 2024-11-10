from pydantic import BaseModel


class AnalyzeSchema(BaseModel):
    id: int
    status: bool  # is_completed
    warning: bool
    reason: str

    def __str__(self) -> str:
        text = f"Карточка #{self.id}:\n"
        if not self.status:
            text += "В процессе проверки."
        elif not self.reason:
            text += "Все проверки пройдены."
        else:
            text += "Недействительна.\n" + self.reason
        if self.warning:
            text += "В карточке есть некритичные ошибки"
        return text
