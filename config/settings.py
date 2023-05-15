
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'anywhere', #dbname
        'HOST': 'database-2.clxvqfgb3dhh.us-east-1.rds.amazonaws.com',
        'PORT': 3306,
        'USER': 'aw_user', #username
        'PASSWORD': 'ab12345!',
    }
}

