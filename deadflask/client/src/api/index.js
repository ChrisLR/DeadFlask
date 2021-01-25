import axios from 'axios';

const srvPath = 'http://localhost:5000';
const axiosConfig = {
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
    'Access-Control-Allow-Origin': 'http://localhost:5000',
    'Access-Control-Allow-Credentials': 'true',
  },
};

function getHeadersJwt(path, jwt) {
  return {
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Access-Control-Allow-Origin': path,
      'Access-Control-Allow-Credentials': 'true',
      // eslint-disable-next-line quote-props
      'Authorization': `Bearer: ${jwt}`,
    },
  };
}

function getHeaders(path) {
  return {
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Access-Control-Allow-Origin': path,
      'Access-Control-Allow-Credentials': 'true',
    },
  };
}

export function fetchBuildingsMap() {
  const path = `${srvPath}/map`;
  return axios.get(path, axiosConfig);
}

export function moveTo(buildingId, jwt) {
  const path = `${srvPath}/move_to`;
  return axios.post(path, { building_id: buildingId }, getHeadersJwt(path, jwt));
}

export function authenticate(userData) {
  const path = `${srvPath}/login`;
  return axios.post(path, userData, getHeaders(path));
}
