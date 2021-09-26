import requests
import json
from utility import keys, URL, API_KEY

class ConvertionException(Exception):
    pass

class valute():
    def __init__(self, quote='', base='', amount=''):
        self.quote = quote
        self.base = base
        self.amount = amount
    
    @property    
    def test_data(self):
        try:
            self.amount = float(self.amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество "{self.amount}"')
            
        if not (self.base in list(keys.keys())):
            raise ConvertionException(f'Неверно введено имя валюты "{self.base}"')
                
        if not (self.quote in list(keys.keys())):
            raise ConvertionException(f'Неверно введено имя валюты "{self.quote}"')

        if self.quote == self.base:
            raise ConvertionException(f'Одинаковые базовая и конвертируемая валюты')

    def convert(self):
        self.test_data
        text = ''
        all_val = ','.join(list(keys.values()))
        r = requests.get(f'{URL}?access_key={API_KEY}&symbols={all_val}&format=1')
        if not r.status_code in range(200,300):
            raise ConvertionException('Не получены данные с сайта')
        r = json.loads(r.content)
        if not r['success']:
            raise ConvertionException('Запрос не прошел')
            
        #text = f'Стоимость валюты {v2} в валюте {v1} в количестве {sum} составляет {(int(r[v2])*sum)}'
        #text = f'{amount} {v1} = {(int(r[keys[v2]])*sum)} {v2}'
        
        ss = round(self.amount * (r['rates'][keys[self.quote]] / r['rates'][keys[self.base]] ),2)
        
        text = f'{self.amount} {self.base} = {ss} {self.quote}'
        return text
    
