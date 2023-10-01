# Currency Converter

Tool to convert given amount (`-a` argument) of money in given currency (`-c` argument) to PLN. Saves the result in JSON database or sqlite database when executed in dev or prod environment (`-e` argument) accordingly.
Uses two sources (`-s` argument) to convert currencies, either a json file (can be customized with `-f` argument), or NBP API.


# Usage

1. Make sure you have python 3.10 or later installed in your local.
2. Make sure you have poetry installed in your local (`pip install poetry`)
3. Activate virtual environment `poetry shell`
4. Install the project `poetry install`
5. (Optional) To run in production environment, create the database `alembic upgrade head`
6. Create `.env` file in project root (see `.env.example`)  
    *Note:* *Caution:* `-e` argument will take precedence over `ENVIRONMENT` environment variable
7. Run the script


# Example usage
```
convert -a 1 -c eur
convert -a 2 -c usd -s nbp -e dev
convert -a 3 -c czk -s local -f source_file.json -e prod
```
