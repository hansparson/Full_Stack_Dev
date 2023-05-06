

### How to Manage ORM DB 
1. make migrate file (alembic), for any change in your models
    <br>`export FLASK_APP=server.py'
    <br>`flask db migrate -d "models/migrations" -m "message"`
    <br> recheck your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.
2. execute migration for your change in db
    <br>`flask db upgrade -d "models/migrations"`