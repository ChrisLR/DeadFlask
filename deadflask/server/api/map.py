from flask import request, jsonify

from deadflask.server.app import app
from deadflask.server.models.buildings import Building, BuildingType
from deadflask.server.auth import require_user


@app.route('/map', methods=['GET'])
@require_user
def get_map(user):
    coordinates = request.args.get('coordinates', (0, 0))
    city = request.args.get('city', 2)
    cx, cy = coordinates
    result_rows = _get_map(cx, cy, city)

    return jsonify(result_rows)


def _get_map(cx, cy, city):
    # Just some quick validation, make something better
    if cx < 0 or cy < 0 or cx > 20000 or cy > 20000:
        cx = 0
        cy = 0

    left = cx - 1
    right = cx + 1
    top = cy - 1
    bottom = cy + 1

    rows = app.db_session.query(Building, BuildingType).filter(
        Building.coord_x >= left,
        Building.coord_x <= right,
        Building.coord_y >= top,
        Building.coord_y <= bottom,
        Building.city == city,
        Building.type == BuildingType.id
    ).order_by(Building.coord_y, Building.coord_x)

    r_array = [[None for _ in range(-1, 2)] for _ in range(-1, 2)]
    for row in rows:
        local_building_x = (row.Building.coord_x - left)
        local_building_y = (row.Building.coord_y - top)
        r_array[local_building_y][local_building_x] = {
                'name': row.Building.name,
                'type': row.BuildingType.name,
                'id': row.Building.id
            }

    return r_array


@app.route('/move_to', methods=['POST'])
@require_user
def move_to(user):
    post_data = request.get_json()
    building_id = post_data.get('building_id', 1)
    building = app.db_session.query(Building).filter(
        Building.id == building_id
    ).first()

    result_rows = _get_map(building.coord_x, building.coord_y, building.city)

    return jsonify(result_rows)
