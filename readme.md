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
