#!/usr/bin/env python
# -*- coding: utf-8 -+-
import sys
import os
import re

usage = """\
usage: parser.py source_file output_file

    source_filename - path to pdf file to extract information
    output_file - path to txt file to store an output information
"""

FETCH_PARAMS = "Параметри запиту"

OBJECT_ADDRESS = "Адреса / Місцезнаходження"
OBJECT_KOD = "Кадастровий номер земельної ділянки"


REGISTRY1 = "ВІДОМОСТІ З ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО"

REGISTRY1_1 = "Актуальна інформація про об’єкт нерухомого майна"

REGISTRY1_1_1 = "Реєстраційний номер об’єкта нерухомого майна"
REGISTRY1_1_2 = "Об’єкт нерухомого майна:"
REGISTRY1_1_3 = "Площа"
REGISTRY1_1_4 = "Кадастровий номер"
REGISTRY1_1_5 = "Цільове призначення"
REGISTRY1_1_6 = "Адреса"
REGISTRY1_1_7 = "Земельні ділянки місця розташування"

REGISTRY1_2 = "Актуальна інформація про право власності"

REGISTRY1_2_1 = "Номер запису про право власності"
REGISTRY1_2_2 = "Дата, час державної реєстрації"
REGISTRY1_2_3 = "Державний реєстратор"
REGISTRY1_2_4 = "Підстава виникнення права власності"
REGISTRY1_2_5 = "Підстава внесення запису"
REGISTRY1_2_6 = "Форма власності"
REGISTRY1_2_7 = "Розмір частки"
REGISTRY1_2_8 = "Власники"
REGISTRY1_2_9 = "Додаткові відомості"

REGISTRY1_3 = "Актуальна інформація про державну реєстрацію іпотеки"

REGISTRY1_3_1 = "Номер запису про іпотеку"
REGISTRY1_3_2 = "Дата, час державної реєстрації"
REGISTRY1_3_3 = "Державний реєстратор"
REGISTRY1_3_4 = "Підстава виникнення іпотеки"
REGISTRY1_3_5 = "Підстава внесення запису"
REGISTRY1_3_6 = "Відомості про основне зобов’язання"
REGISTRY1_3_7 = "Відомості про суб’єктів"
REGISTRY1_3_8 = "Додаткові відомості про іпотеку"


REGISTRY1_4 = "Актуальна інформація про державну реєстрацію обтяжень"

REGISTRY1_4_1 = "Номер запису про обтяження"
REGISTRY1_4_2 = "Дата, час державної реєстрації"
REGISTRY1_4_3 = "Державний реєстратор"
REGISTRY1_4_4 = "Підстава виникнення обтяження"
REGISTRY1_4_5 = "Підстава внесення запису"
REGISTRY1_4_6 = "Вид обтяження"
REGISTRY1_4_7 = "Відомості про суб’єктів обтяження"
REGISTRY1_4_8 = "Відомості про реєстрацію до 01.01.2013р."


REGISTRY2 = "ВІДОМОСТІ З РЕЄСТРУ ПРАВ ВЛАСНОСТІ НА НЕРУХОМЕ МАЙНО"

REGISTRY2_1 = "ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА"

REGISTRY2_1_1 = "Реєстраційний номер майна"
REGISTRY2_1_2 = "Тип майна"
REGISTRY2_1_3 = "Адреса нерухомого майна"
REGISTRY2_1_4 = "Інформація"
REGISTRY2_1_5 = "Номер запису"

REGISTRY2_2 = "ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ"

REGISTRY2_2_1 = "Дата прийняття рішення про державну реєстрацію"
REGISTRY2_2_2 = "Дата внесення запису"
REGISTRY2_2_3 = "ПІБ"
REGISTRY2_2_4 = "Форма власності"
REGISTRY2_2_5 = "Частка власності"
REGISTRY2_2_6 = "Підстава виникнення права власності"


REGISTRY3 = "ВІДОМОСТІ З ЄДИНОГО РЕЄСТРУ ЗАБОРОН ВІДЧУЖЕННЯ ОБ’ЄКТІВ НЕРУХОМОГО МАЙНА"


REGISTRY3_1 = "ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ ДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО"

REGISTRY3_1_1 = "Номер запису про обтяження"
REGISTRY3_1_2 = "Дата перенесення"
REGISTRY3_1_3 = "Запис"

REGISTRY3_2 = "Інформація"

REGISTRY3_2_1 = "Тип обтяження"
REGISTRY3_2_2 = "Реєстраційний номер обтяження"
REGISTRY3_2_3 = "Зареєстровано"
REGISTRY3_2_4 = "Підстава обтяження"
REGISTRY3_2_5 = "Об’єкт обтяження" 
REGISTRY3_2_6 = "Власник"
REGISTRY3_2_7 = "Заявник"
REGISTRY3_2_8 = "Додаткові дані"


REGISTRY4 = "ВІДОМОСТІ З ДЕРЖАВНОГО РЕЄСТРУ ІПОТЕК"

REGISTRY4_1 = "ВІДОМОСТІ ПРО ІПОТЕКУ"

REGISTRY4_1_1 = "Реєстраційний номер обтяження"
REGISTRY4_1_2 = "Тип обтяження"
REGISTRY4_1_3 = "Зареєстровано"
REGISTRY4_1_4 = "Підстава обтяження"
REGISTRY4_1_5 = "Об’єкт обтяження"
REGISTRY4_1_6 = "Іпотекодержатель"
REGISTRY4_1_7 = "Іпотекодавець"
REGISTRY4_1_8 = "Розмір основного зобов’язання"
REGISTRY4_1_9 = "Строк виконання"
REGISTRY4_1_10 = "Заставна"
REGISTRY4_1_11 = "Додаткові дані"


REGISTRY4_2 = "ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ ДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО"

REGISTRY4_2_1 = "Номер запису про іпотеку"
REGISTRY4_2_2 = "Дата перенесення"
REGISTRY4_2_3 = "Запис"


GROUP_ALL = (
	(FETCH_PARAMS,r'Параметри запиту(.*?)ВІДОМОСТІ'),
	(REGISTRY1,
	 r'ВІДОМОСТІ\nЗ ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО\n(.*?)ВІДОМОСТІ'),
	(REGISTRY2,
	 r'ВІДОМОСТІ\nЗ РЕЄСТРУ ПРАВ ВЛАСНОСТІ НА НЕРУХОМЕ МАЙНО\n(.*?)ВІДОМОСТІ\nЗ ЄДИНОГО РЕЄСТРУ'),
	(REGISTRY3,
	 r'ВІДОМОСТІ\nЗ ЄДИНОГО РЕЄСТРУ ЗАБОРОН ВІДЧУЖЕННЯ ОБ’ЄКТІВ НЕРУХОМОГО МАЙНА\n(.*?)ВІДОМОСТІ'),
	(REGISTRY4,
	 r'ВІДОМОСТІ\nЗ ДЕРЖАВНОГО РЕЄСТРУ ІПОТЕК\n(.*?)$'),
)

GROUP_OBJECT = (
	(OBJECT_ADDRESS,
	 r'Адреса /\nМісцезнаходження:\n(.*)[^\n]*'),
	(OBJECT_KOD,
	 r'Кадастровий номер\nземельної ділянки:\n(\d{10}:\d{2}:\d{3}:\d{4})'),
)

GROUP_REG1 = (
	(REGISTRY1_1,
	 r'Реєстраційний номер\nоб’єкта нерухомого\nмайна:\n.*?(?=Реєстраційний|$|Актуальна|відсутні)'),
	(REGISTRY1_2,
	 r'Номер запису про право(?:\n| )власності:.*?(?=Номер|$|Актуальна|відсутні)'),
	(REGISTRY1_3,
	 r'Номер запису про іпотеку:.*?(?=Номер|$|Актуальна|відсутні)'),
	(REGISTRY1_4,
	 r'Номер запису про обтяження:.*?(?=Номер|$|ВІДОМОСТІ|Актуальна|відсутні)'),
)

GROUP_REG2 = (
	(REGISTRY2_1,
	 r'ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА\n(.*?)\nВІДОМОСТІ'),
	(REGISTRY2_2,
	 r'ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ\n(.*?)\n$'),
)

GROUP_REG1_1 = (
	(REGISTRY1_1_1,
	 r'Реєстраційний номер\nоб’єкта нерухомого\nмайна:\n(\d{8,14})\n'),
	(REGISTRY1_1_2,
	 r'Об’єкт нерухомого\nмайна:\n(.*Ні|.*Так)'),
	(REGISTRY1_1_3,r'Площа:(.*?)\n'),
	(REGISTRY1_1_4,
	 r'Кадастровий номер:(\d{10}:\d{2}:\d{3}:\d{4})\n'),
	(REGISTRY1_1_5,
	 r'Цільове призначення:\n(.*)\nАдреса'),
	(REGISTRY1_1_6,r'Адреса:[\n|\s](.*?\d{1,5})\n'),
	(REGISTRY1_1_7,
     r'Земельні ділянки місця.*розташування:\n(.*?)($|Актуальна)'),
)

GROUP_REG1_2 = (
	(REGISTRY1_2_1,r'Номер запису про право(?:\n| )власності:.*?(\d{4,12})'),
	(REGISTRY1_2_2,r'Дата, час державної\nреєстрації:\n(.*? .*?)\n'),
	(REGISTRY1_2_3,r'Державний реєстратор:(.*?)\nПідстава'),
	(REGISTRY1_2_4,r'Підстава виникнення\nправа власності:(.*?)\nПідстава внесення'),
	(REGISTRY1_2_5,r'Підстава внесення\nзапису:\n(.*?)\nФорма власності'),
	(REGISTRY1_2_6,r'Форма власності:(.*?)\n'),
	(REGISTRY1_2_7,r'Розмір частки:(.*?)\n'),
	(REGISTRY1_2_8,r'Власники:(.*?)(Актуальна|Додаткові|Відомості|$)'),
	(REGISTRY1_2_9,r'Додаткові відомості:(.*?)\n(Актуальна|Додаткові|Відомості|$)'),
)

GROUP_REG1_3 = (
	(REGISTRY1_3_1,r'Номер запису про іпотеку:(.*?)\n'),
	(REGISTRY1_3_2,r'Дата, час державної\nреєстрації:\n(.*? .*?)\n'),
	(REGISTRY1_3_3,r'Державний реєстратор:(.*?)\nПідстава'),
	(REGISTRY1_3_4,r'Підстава виникнення\nіпотеки:(.*?)\nПідстава внесення'),
	(REGISTRY1_3_5,r'Підстава внесення\nзапису:\n(.*?)\nВідомості'),
	(REGISTRY1_3_6,r'Відомості про основне\nзобов’язання:\n(.*?)\nВідомості'),
	(REGISTRY1_3_7,r'Відомості про суб’єктів:(.*?)\n(Боржник:|Додаткові.*?:|Відомості.*?:|Адреса.*?:|Опис.*?)'),
	(REGISTRY1_3_8,r'Додаткові відомості про\nіпотеку:\n(.*?)\n(Актуальна|Додаткові|Відомості|$)'),
)
GROUP_REG1_4 = (
	(REGISTRY1_4_1,r'Номер запису про обтяження: (.*?)\n'),
	(REGISTRY1_4_2,r'Дата, час державної\nреєстрації:\n(.*? .*?)\n'),
	(REGISTRY1_4_3,r'Державний реєстратор: (.*?)\nПідстава'),
	(REGISTRY1_4_4,r'Підстава виникнення\nобтяження:\n(.*?)\nПідстава внесення'),
	(REGISTRY1_4_5,r'Підстава внесення\nзапису:\n(.*?)\n(Відомості|Вид|Форма)'),
	(REGISTRY1_4_6,r'Вид обтяження: (.*?)\n(Відомості|$)'),
	(REGISTRY1_4_7,r'Відомості про суб’єктів\nобтяження:(.*?)(Відомості|Вид|Опис|Особа|$)'),
	(REGISTRY1_4_8,r'Відомості про реєстрацію\nдо 01.01.2013р.:\n(.*?)(Відомості|Актуальна|Зміст|$)'),
)

GROUP_REG2_1 = (
	(REGISTRY2_1_1,
	 r'Реєстраційний номер\nмайна:\n(\d{8,14})\n'),
	(REGISTRY2_1_2,
	 r'Тип майна:(.*?)\nАдреса'),
	(REGISTRY2_1_3,r'Адреса нерухомого\nмайна:[\n|\s](.*?\d{1,5})\n'),
	(REGISTRY2_1_4,
	 r'Адреса нерухомого\nмайна:[\n|\s].*?\d{1,5}\n(.*?)\nНомер запису:'),
	(REGISTRY2_1_5,r'Номер запису: (.*?)\.\n'),
)

GROUP_REG2_2 = (
	(REGISTRY2_2_1,
	 r'Дата прийняття рішення\nпро державну\nреєстрацію:\n(.*?)\n'),
	(REGISTRY2_2_2,
	 r'Дата внесення запису: (.*?)\n'),
	(REGISTRY2_2_3,r'ПІБ: (.*?)\n'),
	(REGISTRY2_2_4,
	 r'Форма власності: (.*?)\n'),
	(REGISTRY2_2_5,r'Частка власності: (.*?)\n'),
	(REGISTRY2_2_6,r'Підстава виникнення\nправа власності:\n(.*?)(Відомості|$)'),
)

GROUP_REG3 = (
	(REGISTRY3_1,
	 r'ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ\nДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО\n(.*?)$'),
	(REGISTRY3_2,
	 r'(Тип обтяження:.*?)(?=ВІДМІТКА|$|Актуальна|відсутні)'),
)

GROUP_REG3_1 = (
	(REGISTRY3_1_1,
	 r'Номер запису про\nобтяження:\n(.*)\nДата перенесення'),
	(REGISTRY3_1_2,
	 r'Дата перенесення:(.*?)\n'),
	(REGISTRY3_1_3,r'Дата перенесення:.*?\n(.*?)(ВІДОМОСТІ|$)'),
)

GROUP_REG3_2 = (
	(REGISTRY3_2_1,
	 r'Тип обтяження:(.*?)\n(Реєстраційний)'),
	(REGISTRY3_2_2,
	 r'Реєстраційний номер\nобтяження:\n(.*?)\nЗареєстровано'),
	(REGISTRY3_2_3,r'Зареєстровано:(.*?)\nПідстава обтяження'),
	(REGISTRY3_2_4,r'Підстава обтяження:(.*?)\nОб’єкт обтяження'),
	(REGISTRY3_2_5,r'Об’єкт обтяження: (.*?)\nВласник'),
	(REGISTRY3_2_6,r'Власник: (.*?)\nЗаявник'),
	(REGISTRY3_2_7,r'Заявник: (.*?)(ВІДОМОСТІ|$)'),
	(REGISTRY3_2_8,r'Додаткові дані:(.*?)\n(ВІДМІТКА|$)'),
)


GROUP_REG4 = (
	(REGISTRY4_1,
	 r'(Реєстраційний номер.*)\n(?:ВІДМІТКА|$)'),
	(REGISTRY4_2,
	 r'ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ\nДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО\n(.*?)$'),
)

GROUP_REG4_1 = (
	(REGISTRY4_1_1,
	 r'Реєстраційний номер\nобтяження:\n(.*?)\n'),
	(REGISTRY4_1_2,
	 r'Тип обтяження: (.*?)\nЗареєстровано'),
	(REGISTRY4_1_3,r'Зареєстровано: (.*?)\nПідстава обтяження'),
	(REGISTRY4_1_4,
	 r'Підстава обтяження: (.*?)\nОб’єкт'),
	(REGISTRY4_1_5,
	 r'Об’єкт обтяження: (.*?)\nЧастково'),
	(REGISTRY4_1_6,r'Іпотекодержатель: (.*?)\nІпотекодавець'),
	(REGISTRY4_1_7,
	 r'Іпотекодавець: (.*?)\nРозмір'),
	(REGISTRY4_1_8,
	 r'Розмір основного\nзобов’язання:\n(.*?)\nСтрок'),
	(REGISTRY4_1_9,r'Строк виконання: (.*?)\n'),
	(REGISTRY4_1_10,
	 r'Заставна: (.*?)\nДодаткові'),
	(REGISTRY4_1_11,
	 r'Додаткові дані: (.*?)$'),
)

GROUP_REG4_2 = (
	(REGISTRY4_2_1,
	 r'Номер запису про\nіпотеку:(.*?)\nДата перенесення'),
	(REGISTRY4_2_2,
	 r'Дата перенесення:(.*?)\n'),
	(REGISTRY4_2_3,r'Дата перенесення:.*?\n(.*?)$'),
)


def separate(data,GROUP_PARAMS):
	dic = {}
	for group in GROUP_PARAMS:
		for param1,param2 in [group]:
			p = re.search(param2,data,re.U|re.S)
			dic[param1] = p.group(1) if p else "None"
	return dic

def group_reg(data,GROUP_PARAMS):
	lst = []
	for i in xrange(len(data)):
		if data[i]:
			lst.append(separate(data[i],GROUP_PARAMS))
	return lst

def reg(data,GROUP_PARAMS):
	dic = {}
	for group in GROUP_PARAMS:
		for param1,param2 in [group]:
			p = re.findall(param2,data,re.U|re.S)
			dic[param1] = p if p else "None"	
	return dic


if __name__ == "__main__":
	source_file = ''
	output_file = ''
	
	if  len(sys.argv) < 3 : sys.exit(usage)
	elif len(sys.argv) > 2: 
		source_file = sys.argv[1]
		output_file = sys.argv[2]

		"""
		pdftotext - is installed poppler-utils package for PDF to text conversion;

		keys:
			-raw   Keep the text in content stream order;
			-nopgbrk  Don’t insert page breaks between  pages.
		""" 
		os.system(('pdftotext -raw -nopgbrk {0} {1}').format( 
					source_file, output_file))
		with open(output_file,'rb') as f:
			text = f.read()		#converted text from pdf file
			text = re.sub(r'стор. \d{1,3} з \d{1,3}|RRP-.*?\n','',text) #deletes junk
			check = separate(text,GROUP_ALL) #first level separation
			#params of qwery
			check[FETCH_PARAMS] = separate(check[FETCH_PARAMS],GROUP_OBJECT)
			#1
			check[REGISTRY1] = reg(check[REGISTRY1],GROUP_REG1)
			#1-1
			check[REGISTRY1][REGISTRY1_1] = group_reg(check[REGISTRY1][REGISTRY1_1],GROUP_REG1_1)
			#1-2
			check[REGISTRY1][REGISTRY1_2] = group_reg(check[REGISTRY1][REGISTRY1_2],GROUP_REG1_2)
			#1-3
			check[REGISTRY1][REGISTRY1_3] = group_reg(check[REGISTRY1][REGISTRY1_3],GROUP_REG1_3)
			#1-4
			check[REGISTRY1][REGISTRY1_4] = group_reg(check[REGISTRY1][REGISTRY1_4],GROUP_REG1_4)
			#2
			check[REGISTRY2] = reg(check[REGISTRY2],GROUP_REG2)
			#2-1
			check[REGISTRY2][REGISTRY2_1] = group_reg(check[REGISTRY2][REGISTRY2_1],GROUP_REG2_1)
			#2-1
			check[REGISTRY2][REGISTRY2_2] = group_reg(check[REGISTRY2][REGISTRY2_2],GROUP_REG2_2)
			#3
			check[REGISTRY3] = reg(check[REGISTRY3],GROUP_REG3)
			#3-1
			check[REGISTRY3][REGISTRY3_1] = group_reg(check[REGISTRY3][REGISTRY3_1],GROUP_REG3_1)
			#3-2

			check[REGISTRY3][REGISTRY3_2] = group_reg(check[REGISTRY3][REGISTRY3_2],GROUP_REG3_2)
			#4
			#print check[REGISTRY4]
			check[REGISTRY4] = reg(check[REGISTRY4],GROUP_REG4)
			#4-1
			check[REGISTRY4][REGISTRY4_1] = group_reg(check[REGISTRY4][REGISTRY4_1],GROUP_REG4_1)
			#4-2
			check[REGISTRY4][REGISTRY4_2] = group_reg(check[REGISTRY4][REGISTRY4_2],GROUP_REG4_2)
			
			print check
			#end
