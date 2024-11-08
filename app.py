from flask import Flask
from config import Config
from models import db, Room, Guest, Booking, User
from routes import main
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных
db.init_app(app)

# Создание таблиц (если они не были созданы)
with app.app_context():
    db.create_all()

# Регистрация маршрутов
app.register_blueprint(main)

# Настройка админ-панели
admin = Admin(app, name='Hotel Management', template_mode='bootstrap3')
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(Guest, db.session))
admin.add_view(ModelView(Booking, db.session))
admin.add_view(ModelView(User, db.session))

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
