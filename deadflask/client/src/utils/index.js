import Vue from 'vue';
import axios from 'axios';

const loginUrl = 'http://localhost:5000/login/';

export const EventBus = new Vue();

export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1]));
  const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds since epoch
  const now = new Date();
  return now < exp;
}

export function authenticate(_email, _password) {
  return axios.post(loginUrl, { email: _email, password: _password });
}
