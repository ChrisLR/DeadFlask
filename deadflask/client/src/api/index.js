import axios from 'axios';

const srvPath = 'http://localhost:5000';
const axiosConfig = {
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
    'Access-Control-Allow-Origin': 'http://localhost:5000',
  },
};

export function fetchBuildingsMap() {
  const path = `${srvPath}/map`;
  return axios.get(path, axiosConfig);
}

export function moveTo(buildingId) {
  const path = `${srvPath}/move_to`;
  return axios.post(path, { building_id: buildingId }, axiosConfig);
}
