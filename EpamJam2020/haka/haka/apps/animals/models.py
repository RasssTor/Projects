from django.db import models

class Animal(models.Model):
	animal_name = models.CharField('Имя животного', max_length = 50)
	animal_class = models.CharField('Тип животного', max_length = 30)
	animal_description = models.CharField('Описание животного', max_length = 60)
	pub_date = models.DateTimeField('Дата публикации')
	animal_sex = models.CharField('Пол', max_length = 20)
	animal_age = models.IntegerField('Возраст', default = 0)
	vk_url = models.CharField("Ссылка вк", max_length = 40, default = "lol")
	model_pic = models.ImageField(upload_to = 'haka/apps/animals/static/upload', default = 'static/')


	def __str__(self):
		return self.animal_name

	