from app.schemas.user import UserSchema, CheckCriteriaSchema


class UserRepository:
    models = []

    def __init__(self):
        pass

    def _make(self, telegram_id: int) -> UserSchema:
        return UserSchema(telegram_id=telegram_id, criteria=CheckCriteriaSchema())

    def store(self, telegram_id: int):
        saved_model = self.get(telegram_id)
        if saved_model is not None:
            return saved_model
        model = self._make(telegram_id)
        self.models.append(model)
        return model

    def get(self, model_id: int) -> UserSchema | None:
        for m in self.models:
            if m.telegram_id == model_id:
                return m

    def toggle_criteria(self, model_id: int, criteria_name: str) -> UserSchema | None:
        for i in range(len(self.models)):
            if self.models[i].telegram_id == model_id:
                self.models[i].criteria.__dict__.update({criteria_name: not getattr(self.models[i].criteria, criteria_name)})
                return self.models[i]
