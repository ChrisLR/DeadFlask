import axios from 'axios';

const srvPath = 'http://localhost:5000';

function getHeadersJwt(path) {
  return {
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Access-Control-Allow-Origin': path,
      'Access-Control-Allow-Credentials': 'true',
      // eslint-disable-next-line quote-props
      'Authorization': `Bearer: ${localStorage.token}`,
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
  return axios.get(path, getHeadersJwt(path));
}

export function moveTo(buildingId) {
  const path = `${srvPath}/move_to`;
  return axios.post(path, { building_id: buildingId }, getHeadersJwt(path));
}

export function authenticate(userData) {
  const path = `${srvPath}/login`;
  return axios.post(path, userData, getHeaders(path));
}

export function createCharacter(characterData) {
  const path = `${srvPath}/character`;
  return axios.post(path, characterData, getHeadersJwt(path));
}

export function getCharacterTypes() {
  const path = `${srvPath}/character/types`;
  return axios.get(path, getHeadersJwt(path));
}

export function fetchCharacterInfo(characterId) {
  const path = `${srvPath}/character/${characterId}`;
  return axios.get(path, getHeadersJwt(path));
}

export function fetchCharacters() {
  const path = `${srvPath}/character`;
  return axios.get(path, getHeadersJwt(path));
}
