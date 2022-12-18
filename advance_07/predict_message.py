class SomeModel:
    def predict(self, message: str) -> float:
        num_digits_len = len(str(len(message)))
        return len(message) / (10 ** num_digits_len)


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8
) -> str:
    pred = model.predict(message)
    if pred < bad_thresholds:
        return "неуд"

    if pred > good_thresholds:
        return "отл"

    return "норм"
