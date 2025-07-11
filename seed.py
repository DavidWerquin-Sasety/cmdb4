
from app import create_app
from app.extensions import db
from app.models.core import Client, Site, SiteType
import random
import string
from datetime import date

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

def rand_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

client = Client(name="Client Demo")
db.session.add(client)
db.session.commit()

site_type = SiteType(client=client, label="Datacenter")
db.session.add(site_type)
db.session.commit()

for i in range(3):
    site = Site(client=client,
                name=f"Site {i}",
                code=rand_code(),
                type_id=site_type.id,
                street="1 rue Exemple",
                postal_code="75000",
                city="Paris",
                country="France")
    db.session.add(site)
db.session.commit()

print("Base de données remplie avec des données de test.")
