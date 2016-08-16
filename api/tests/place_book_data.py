from datetime import datetime, timedelta

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

bad_place_book_1 = {
	'user_id': 404,
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
	'is_validated': True,
	'number_nights': 1
}

bad_place_book_4 = {
	'user_id': 'Nope',
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_5 = {
	'user_id': 1,
	'is_validated': 'Nope',
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 1
}

bad_place_book_6 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': 400,
	'number_nights': 1
}

bad_place_book_7 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': '2016/07/24',
	'number_nights': 1
}

bad_place_book_8 = {
	'user_id': 1,
	'is_validated': True,
	'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 'Nope'
}

bad_date_9 = datetime.now() + timedelta(days=1)

bad_place_book_9 = {
	'user_id': 2,
	'is_validated': False,
	'date_start': bad_date_9.strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 2
}

bad_date_10 = datetime.now() - timedelta(days=2)

bad_place_book_10 = {
	'user_id': 2,
	'is_validated': False,
	'date_start': bad_date_10.strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 3
}

bad_date_11 = datetime.now() - timedelta(days=2)

bad_place_book_11 = {
	'user_id': 2,
	'is_validated': False,
	'date_start': bad_date_11.strftime("%Y/%m/%d %H:%M:%S"),
	'number_nights': 6
}
