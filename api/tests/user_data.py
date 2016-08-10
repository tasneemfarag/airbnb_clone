good_user_1 = {
    'email': 'jon.snow@superawesome.com',
    'first_name': 'Jon',
    'last_name': 'Snow',
    'is_admin': True,
    'password': 'test1234'
}

good_user_2 = {
    'email': 'sally.strong@superawesome.com',
    'first_name': 'Sally',
    'last_name': 'Strong',
    'is_admin': True,
    'password': 'test1234'
}

bad_user_1 = {
    'first_name': 'Joe',
    'last_name': 'Strong',
    'is_admin': True,
    'password': 'test1234'
}

bad_user_2 = {
    'email': 'joe.strong@superawesome.com',
    'last_name': 'Strong',
    'is_admin': False,
    'password': 'test1234'
}

bad_user_3 = {
    'email': 'joe.strong@superawesome.com',
    'first_name': 'Joe',
    'is_admin': False,
    'password': 'test1234'
}

bad_user_4 = {
    'email': 'joe.strong@superawesome.com',
    'first_name': 'Joe',
    'last_name': 'Strong',
	'is_admin': False,
}

bad_user_5 = {
    'email': 400,
    'first_name': 'Sally',
    'last_name': 'Strong',
    'is_admin': True,
    'password': 'test1234'
}

bad_user_6 = {
    'email': 'sally.strong@superawesome.com',
    'first_name': 400,
    'last_name': 'Strong',
    'is_admin': True,
    'password': 'test1234'
}

bad_user_7 = {
    'email': 'sally.strong@superawesome.com',
    'first_name': 'Sally',
    'last_name': 400,
    'is_admin': True,
    'password': 'test1234'
}

bad_user_8 = {
    'email': 'sally.strong@superawesome.com',
    'first_name': 'Sally',
    'last_name': 'Strong',
    'is_admin': 'Nope',
    'password': 'test1234'
}

bad_user_9 = {
    'email': 'sally.strong@superawesome.com',
    'first_name': 'Sally',
    'last_name': 'Strong',
    'is_admin': True,
    'password': 400
}
