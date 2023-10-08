from app import db, House, Agent, User, app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.app_context().push()

house1 = House(
    title="Roracio House",
    size=2000,
    price=4500000,
    description="Middle Family House",
    city="Kilimani",
    county="Nairobi",
    bedrooms=3,
    bathrooms=2,
    # image_paths=["https://langatalinkrealestate.com/wp-content/uploads/2023/07/KAR222S-1.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/07/KAR222S-3.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/07/KAR222S-1-2.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/07/KAR222S-2.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/07/KAR222S-4.jpg"],
    image_paths="https://langatalinkrealestate.com/wp-content/uploads/2023/07/KAR222S-1.jpg",
    agent_id=1
)

house2 = House(
    title="Osoro&Family House",
    size=3000,
    price=4500000,
    description="House of memories, located on a serene environment",
    city="Upperhill",
    county="Nairobi",
    bedrooms=4,
    bathrooms=2,
    # image_paths=["https://langatalinkrealestate.com/wp-content/uploads/2023/03/KAR302S-1-1.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/03/KAR302S-2.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/03/KAR302S-4.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/03/KAR302S-5.jpg", "https://langatalinkrealestate.com/wp-content/uploads/2023/03/KAR302S-7.jpg"],
    image_paths="https://langatalinkrealestate.com/wp-content/uploads/2023/03/KAR302S-1-1.jpg",
    agent_id=2
)

agent1 = Agent(
    name="Faith Kaburu",
    phonebook="0789126352",
    email="faithkaburu@gmail.com",
    username="faithkaburu@gmail.com",
    password="faith"
    # password_hash=bcrypt.generate_password_hash("faith").decode('utf-8')  # Hash the password here
)
agent1.set_password("faith")

agent2 = Agent(
    name="Emmanual Peter",
    phonebook="0796325841",
    email="peter@gmail.com",
    username="emmanuelpeter@gmail.com",
    password="peter"
    # password_hash=bcrypt.generate_password_hash("peter").decode('utf-8')  # Hash the password here
)
agent2.set_password("peter")

user1 = User(
    email="prince@gmail.com",
    password="prince"
    # password_hash=bcrypt.generate_password_hash("prince").decode('utf-8')  # Hash the password here
)
user1.set_password("prince")

user2 = User(
    email="faithkaburu@gmail.com",
    password="sumeya"
    # password_hash=bcrypt.generate_password_hash("sumeya").decode('utf-8')  # Hash the password here
)
user2.set_password("sumeya")


db.session.add_all([house1, house2, agent1, agent2, user1, user2])
db.session.commit()

print("Data added to the database successfully!")

