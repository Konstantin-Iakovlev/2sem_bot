from typing import List, NamedTuple, Optional
import db
import exceptions
import datetime


class Translation(NamedTuple):
    id_: Optional[int]
    src: str
    trg: str
    created: str


def add_translation(raw_message: str) -> Translation:
    try:
        src, trg = raw_message.split()
    except:
        raise exceptions.NotCorrectMessage(
            'Неверный формат добавления. Введите в формате: <english> <russian>')
    translation = Translation(id_=None, src=src, trg=trg,
                              created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    _ = db.insert("words", {
        "src": translation.src,
        "trg": translation.trg,
        "created": translation.created,
    })
    return translation


def last() -> List[Translation]:
    """Возвращает последние несколько переводов"""
    cursor = db.get_cursor()
    cursor.execute(
        "select id, src, trg, created from words order by created desc limit 10"
    )
    rows = cursor.fetchall()
    last_translations = [Translation(
        id_=id_, src=src, trg=trg, created=created) for id_, src, trg, created in rows]
    return last_translations
