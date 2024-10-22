# Database structure
![Gaspromik drawio](https://github.com/user-attachments/assets/87d6a00f-0438-463b-89b4-9a32d0c63e36)

# Global backend structure simplified
![GazpromikStrucrure drawio](https://github.com/user-attachments/assets/cc698b97-169f-4ee6-ad72-410f02a69be7)

# Запуск и работа сервера  

Перед запуском обязательно скачать зависимости, с помощью pip или других инструментов:  
```$ pip install -r ./requirements.txt```

Перед запуском сервера необходимо создать PostgreSql сервер и создать в нём базу данных с следующими параметрами:  
**database name**: *gazpromik*  
**PG_USER**: *postgres*  
**PG_PASSWORD**: *pgAdminPassword*  
**PG_PORT**: *5432*  
**PG_HOST**: *localhost*  
> Можно сделать это, например, через pgadmin4.  
> Эти параметры также можно изменить на ваше усмотрение, установив переменные среды с соответсвующими ключами, как в ```enviroments.py```

**Команда запуска**   
```$ python start.py```  

## Отладка сервера  
Для отладки и тестирования всего функционала можно заходить на ```http://127.0.0.1:8080/api/docs```, где в доступной форме можно посылать запросы на сервер и получать ответы.  


# Используемые технологии  
## FastAPI  
![image](https://github.com/user-attachments/assets/3cd2fa03-d28b-41fb-9e73-b59b5cb25401)  
> Для Бэкенда.
> Потому что fast и потому что API
## SQLalchemy  
![image](https://github.com/user-attachments/assets/8ed7b10a-dfaf-4db5-87ed-b2a2049112e7)  
> Для работы с базой данных  
## Llama cpp  
![image](https://github.com/user-attachments/assets/a7de8ff9-b0b0-4d32-80e1-7400f2a4bba9)  
> Для работы с LLM  
