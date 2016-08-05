from datetime import datetime

good_place_book_1 = {
	'user_id': 2,
	'is_validated': False,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 2
}

good_place_book_2 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_2 = {
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_3 = {
	'user_id': 1,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_4 = {
	'user_id': 1,
	'is_validated': True,
	'number_nights': 1
}

bad_place_book_5 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S")
}

bad_place_book_7 = {
	'user_id': '500',
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_8 = {
	'user_id': 1,
	'is_validated': 'Nope',
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_9 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': '2016/07/24',
	'number_nights': 1
}

bad_place_book_10 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': '10'
}
