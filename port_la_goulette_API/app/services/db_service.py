# from extensions import db
# from models.service import Service

# # Get all services
# def get_all_services():
#     try:
#         services = Service.query.all()
#         return [service.to_dict() for service in services]
#     except Exception as e:
#         return {"error": str(e)}

# # Get a specific service by ID
# def get_service_by_id(service_id):
#     try:
#         service = Service.query.get(service_id)
#         if service:
#             return service.to_dict()
#         return None
#     except Exception as e:
#         return {"error": str(e)}
from extensions import db
from models.service import Service

# Get all services
def get_all_services():
    try:
        services = Service.query.all()
        return [
            {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price,
                "is_available": service.is_available
            } for service in services
        ]
    except Exception as e:
        return {"error": str(e)}

# Get a specific service by ID
def get_service_by_id(service_id):
    try:
        service = Service.query.get(service_id)
        if service:
            return {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price,
                "is_available": service.is_available
            }
        return None
    except Exception as e:
        return {"error": str(e)}

# Create a new service
def create_service(data):
    try:
        new_service = Service(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            is_available=data.get("is_available", True)
        )
        db.session.add(new_service)
        db.session.commit()
        return {
            "id": new_service.id,
            "name": new_service.name,
            "description": new_service.description,
            "price": new_service.price,
            "is_available": new_service.is_available
        }
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# Update an existing service
def update_service(service_id, data):
    try:
        service = Service.query.get(service_id)
        if not service:
            return None
        
        for key, value in data.items():
            if value is not None:
                setattr(service, key, value)
        db.session.commit()
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "is_available": service.is_available
        }
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
