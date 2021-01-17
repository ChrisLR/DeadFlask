from deadflask.server.app import app
from deadflask.server.models.buildings import Building, BuildingType
from flask import request, jsonify


@app.route('/map', methods=['GET'])
def get_map():
    coordinates = request.args.get('coordinates', (0, 0))
    city = request.args.get('city', 2)
    cx, cy = coordinates
    # Just some quick validation, make something better
    if cx < 0 or cy < 0 or cx > 20000 or cy > 20000:
        cx = 0
        cy = 0

    rows = app.db_session.query(Building, BuildingType).filter(
        Building.coord_x >= cx,
        Building.coord_x < cx + 10,
        Building.coord_y >= cy,
        Building.coord_y < cy + 10,
        Building.city == city,
        Building.type == BuildingType.id
    ).order_by(Building.coord_y, Building.coord_x)

    result = [
        {'name': row.Building.name, 'type': row.BuildingType.name, 'coordinates': (row.Building.coord_x, row.Building.coord_y)}
        for row in rows
    ]

    return jsonify(result)
