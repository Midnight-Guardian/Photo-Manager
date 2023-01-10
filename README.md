# Photo-Manager
Тестовое задание.

Сделать REST фото менеджер.
1) загружать фотографии авторизованным пользователям.
  1.1) при загрузке можно указывать различную метадату: гео локацию, описание, имена людей на фото.
2) отображать список фотографий, без мета данных.
  2.1) фильтровать фотографии по дате.
  2.2) фильтровать фотографии по геолокации.
  2.3) фильтровать фотографии по имени человека.
3) получать фотографию по айди с метаданными.
4) доп задача: сделать апи автодополнение по поиску возможных имен людей присутствующих на фотографиях. 
  Пример:
  передаем часть имени “Алекс”
  на выходе получаем
  Алекс
  Алексей
  Александр
  Александра
