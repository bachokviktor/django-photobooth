# Parmelian

Social network written in Python Django.

## Installation

Clone the repository

``` bash
git clone https://github.com/bachokviktor/parmelian-social-network.git
cd parmelian-social-network
```

Create a virtual environment

``` bash
python -m venv venv
source venv/bin/activate
```

Install dependencies

``` bash
pip install -r requirements.txt
```

Set the environent variables in `.env.example` and rename it to `.env`

``` bash
mv .env.example .env
```

Run migrations

``` bash
python manage.py migrate
```

Run the development server

``` bash
python manage.py runserver
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
