from models.ship import Ship
from models.service import Service  # Assuming you have a Service model to manage services offered in the port
from extensions import db
from schemas import PlainShipSchema

# Get all ships
def get_all_ships():
    return Ship.query.all()

# Get a specific ship by ID
def get_ship_by_id(id):
    return Ship.query.get(id)

# Get ships by their status (e.g., docked, arrived, departed)
def get_ships_by_status(status):
    ships = Ship.query.filter_by(status=status).all() 
    return ships

# Update ship status
def update_ship_status(id, new_status):
    ship = Ship.query.get(id)
    if ship:
        ship.status = new_status
        db.session.commit()  # Save the changes to the database
        return ship
    return None



def create_ship(name, type, arrival_time, departure_time=None, status="arrived"):
    ship = Ship(
        name=name,
        type=type,
        arrival_time=arrival_time,
        departure_time=departure_time,
        status=status,
    )
    db.session.add(ship)
    db.session.commit()
    return PlainShipSchema().dump(ship)




# Link a ship to a service (like docking, parking)
def link_ship_to_service(ship_id, service_id):
    ship = Ship.query.get(ship_id)
    service = Service.query.get(service_id)
    if ship and service:
        # Example: Associate ship with a specific service
        ship.services.append(service)
        db.session.commit()  # Save the changes
        return ship
    return None
