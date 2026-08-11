import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = Path.home() / 'Desktop' / 'Грэйдстрой проекты'
dest = root / 'public' / 'img' / 'projects'

map = {
    'iron-trade-sklad': ['Айрон Трейд.jpg', 'Айрон Трейд 2.jpg', 'Айрон Трейд 3.jpg'],
    'akron-karbamid': ['Акрон.jpg', 'Акрон 2.jpg'],
    'aneliya-sportkompleks': ['Анелия.jpg', 'Анелия 2.jpg'],
    'glavuks-detsad': ['ГлавУКС.jpg', 'ГлавУКС 2.jpg', 'ГлавУКС 3.jpg'],
    'delovye-linii-sklad': ['ДеловыеЛинии.jpg', 'ДеловыеЛинии 2.jpg', 'ДеловыеЛинии 3.jpg'],
    'pysin-smolensk': [
        'ИП Пысин.jpg', 'ИП Пысин 2.jpg', 'ИП Пысин 3.jpg',
        'ИП Пысин 4.jpg', 'ИП Пысин 5.jpg', 'ИП Пысин 6.jpg',
    ],
    'intellektualnye-sistemy-nn': ['ИС НН.jpg', 'ИС НН 2.jpg', 'ИС НН 3.jpg'],
    'homa-korpus-16': ['Компания Хома.jpg', 'Компания Хома 2.jpg'],
    'korund-cian': ['Корунд-Циан.jpg', 'Корунд-Циан 2.jpg'],
    'sibur-neftekhim': ['Сибур-Нефтехим.jpg'],
    'sintez-oka': ['Синтез ОКА.jpg', 'Синтез ОКА 2.jpg'],
    'tehnonikol-nn': ['ТехноНикель НН.jpg', 'ТехноНикель НН 2.jpg', 'ТехноНикель НН 3.jpg'],
    'farm-konstrakshen': ['Фарм Констракшен.jpg', 'Фарм Констракшен 2.jpg'],
    'hemkor': ['ХЕМКОР.jpg', 'ХЕМКОР 2.jpg'],
}

for project_id, files in map.items():
    out_dir = dest / project_id
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(files, start=1):
        src_file = src / name
        dst_file = out_dir / f'{i:02d}.jpg'
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f'OK {project_id}/{dst_file.name}')
        else:
            print(f'MISSING {src_file}')

print('Done')
