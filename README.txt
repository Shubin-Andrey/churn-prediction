python-flask-docker
Итоговый проект (пример) курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy API: flask Данные: churn_data.csv

Задача: предсказать по описанию пользователя собирается ли он уйти в отток или нет (поле Exited). Бинарная классификация

Используемые признаки:

Категориальные признаки: 'Geography', 'Gender', 'Tenure', 'HasCrCard', 'IsActiveMember'
Числовые признаки:'CreditScore', 'Age', 'Balance', 'NumOfProducts', 'EstimatedSalary'

Преобразования признаков: Категориальные- OneHotEncoder
			  Числовые- Получение степеней и логарифма признаков, Масштабирование признаков(RobustScaler), Получение главных компонент(PCA) 

Модель: XGBoost

Клонируем репозиторий и создаем образ
$ git clone https://github.com/Shubin-Andrey/churn-prediction.git
$ cd churn-prediction
$ docker build -t churn-prediction .
Запускаем контейнер


$ docker run -d -p 8180:8180 -p 8181:8181 -v Shubin-Andrey/churn-prediction
Переходим на localhost:8181