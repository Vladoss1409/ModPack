#!/usr/bin/env python3
"""Write missing Patchouli progress (chronicle) entries for T2–T5."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "overrides" / "patchouli_books" / "expedition_journal" / "en_us" / "entries" / "progress"

ENTRIES = [
    ("t2_w1", "T2: промышленный старт", "kubejs:journal_page_cell_01", "t2_lore_w1", 21,
     "$(bold)Mek и EIO на базе$()$(br2)Стальной корпус, инфузер, обогатитель — завод ожил. Руда идёт через цепочку, я перестал считать слитки вручную.$(br2)$(italic)«Thermal научил терпению. Mek требует масштаба.»$()"),
    ("t2_w2", "T2: энергоузел", "kubejs:journal_page_cell_02", "t2_lore_w2", 22,
     "$(bold)Энергия и переработка$()$(br2)Дробитель, куб, сплавная печь, Flux — контур держится. Второй рубеж T2 в журнале."),
    ("t2_w3", "T2: готовность к сети", "kubejs:journal_page_cell_03", "t2_lore_w3", 23,
     "$(bold)Перед матрицей$()$(br2)Осмий, вибрант, схемы — в ящиках. Чертёж $(#FFAA00)якорной матрицы$() пульсирует в блокноте."),
    ("t3_w1", "T3: сеть зарождается", "kubejs:journal_page_matrix_01", "t3_lore_w1", 31,
     "$(bold)Фундамент AE2$()$(br2)Гравёр, certus, fluix, камень философов — сеть обрела глаза и руки."),
    ("t3_w2", "T3: ME-сеть работает", "kubejs:journal_page_matrix_02", "t3_lore_w2", 32,
     "$(bold)Контроллер пульсирует$()$(br2)Процессоры, терминал, диски — склад стал единым организмом. Второй рубеж T3 закрыт."),
    ("t3_w3", "T3: готовность к Draconic", "kubejs:journal_page_matrix_03", "t3_lore_w3", 33,
     "$(bold)Логистика замкнута$()$(br2)Автокрафт и шины снабжают базу сами. Осталось собрать $(#FFAA00)сингулярность$()."),
    ("t4_intro", "T4: порог Draconic", "kubejs:journal_page_singularity_00", "t4_lore_intro", 40,
     "$(bold)Сингулярность открыла дракона$()$(br2)Новая глава: $(#DD55DD)Draconic Evolution$(). Первый шаг — $(#FFAA00)ядро дракония$(). Chaos Guardian ждёт в конце тира.$(br2)$(italic)«Сеть помнила каждый болт. Дракон помнит каждую эпоху.»$()"),
    ("t4_w1", "T4: драконий старт", "kubejs:journal_page_singularity_01", "t4_lore_w1", 41,
     "$(bold)Draconic на базе$()$(br2)Ядро, пыль, энергоядро, awakened-слиток — фундамент драконьей ветки заложен."),
    ("t4_w2", "T4: энергия дракона", "kubejs:journal_page_singularity_02", "t4_lore_w2", 42,
     "$(bold)Сила на пике$()$(br2)Инфузор, реактор, EMC, хаос-осколки — энергия дракона течёт через базу."),
    ("t4_w3", "T4: готовность к нексусу", "kubejs:journal_page_singularity_03", "t4_lore_w3", 43,
     "$(bold)Chaos позади$()$(br2)Страж повержен, компоненты нексуса собраны. Чертёж сходится в одной точке."),
    ("t4_finale", "T4: якорный нексус", "kubejs:journal_page_singularity_04", "t4_lore_finale", 44,
     "$(bold)Нексус собран$()$(br2)Все тиры сходятся в $(#FFAA00)якорном нексусе$(). Порог T4→T5 пройден — впереди $(#DD55DD)next_ae$()."),
    ("t5_intro", "T5: порог next_ae", "kubejs:journal_page_nexus_00", "t5_lore_intro", 50,
     "$(bold)Финальная глава$()$(br2)$(#FFAA00)Якорный нексус$() открыл $(#DD55DD)next_ae$() и путь к $(#DD55DD)Ядру реальности$().$(br2)$(italic)«Последний чертёж. После — тишина или конец разлома.»$()"),
    ("t5_w1", "T5: next_ae запущен", "kubejs:journal_page_nexus_01", "t5_lore_w1", 51,
     "$(bold)Ядро машины$()$(br2)next_ae ожил, осколки стабилизированы. Первый рубеж финального тира закрыт."),
    ("t5_w2", "T5: осколки сходятся", "kubejs:journal_page_nexus_02", "t5_lore_w2", 52,
     "$(bold)Синхронизация$()$(br2)Inscriber, зарядник, резонансный маяк — круг осколков замыкается."),
    ("t5_w3", "T5: готовность к ядру", "kubejs:journal_page_nexus_03", "t5_lore_w3", 53,
     "$(bold)Перед ритуалом$()$(br2)Сборка якоря, кооп-синхрон, стабилизация — всё готово к рождению ядра."),
    ("t5_finale", "T5: ядро якоря", "kubejs:journal_page_nexus_04", "t5_lore_finale", 54,
     "$(bold)Экспедиция завершена$()$(br2)$(#DD55DD)Ядро Якоря реальности$() стабилизировано. Разлом затих. Мы выстояли."),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for file_stem, name, icon, adv, sortnum, text in ENTRIES:
        entry = {
            "name": name,
            "icon": icon,
            "category": "patchouli:progress",
            "advancement": f"cooptech:journal/{adv}",
            "secret": True,
            "sortnum": sortnum,
            "pages": [{"type": "patchouli:text", "text": text}],
        }
        path = OUT / f"{file_stem}.json"
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {path.name}")


if __name__ == "__main__":
    main()
