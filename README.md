# Camera Relax Monitoring

Данный скрипт использует вебкамеру для мониторинга активности пользователя и напоминает о необходимости делать 
перерывы во время работы за компьютером. Если пользователь проводит за компьютером непрерывно 30 минут, 
программа автоматически предложит сделать перерыв. Для сброса уведомления необходимо отойти от рабочего места 
на 3 минуты. После этого можно будет продолжить работу. Также предусмотрена функция отложить перерыв на 5 минут.

```sh
pip install pipenv
pipenv install
pipenv run .\main.py
```
