# python-flask-docker
Итоговый проект курса "Машинное обучение в бизнесе"

ML: sklearn, pandas, numpy
API: flask
Данные: с kaggle - https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction

Задача: предсказать по описанию вакансии является ли она фейком или нет (поле fraudulent). Бинарная классификация

Используемые признаки:

- title (text)
- description (text)
- company_profile (text)
- benefits (text)
- has_company_logo (int)
- has_questions (int)
- requirements (text)
- industry (text)
- function (text)


Преобразования признаков: tfidf

Модель: xgboost

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/YulyaOfitserova/GB_docker_flask
$ cd GB_docker_flask
$ docker build -t gb_docker_flask .
```

### Запускаем контейнер

```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models 
gb_docker_flask .
...

 ### Переходим на localhost:8181
