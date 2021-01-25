/* eslint-disable no-shadow */
import Vue from 'vue';
import Vuex from 'vuex';
import { isValidJwt, EventBus } from '../utils';
import { fetchBuildingsMap, moveTo, authenticate } from '../api/index';

Vue.use(Vuex);

const state = {
  // single source of data
  buildingsMap: [],
  user: {},
  jwt: '',
};

const actions = {
  // asynchronous operations
  loadBuildingsMap(context) {
    return fetchBuildingsMap().then((response) => context.commit('setBuildingsMap', response.data));
  },
  moveToBuilding(context, { buildingId }) {
    return moveTo(buildingId).then((response) => context.commit('setBuildingsMap', response.data));
  },
  login(context, userData) {
    context.commit('setUserData', { userData });
    return authenticate(userData)
      .then((response) => context.commit('setJwtToken', { jwt: response.data }))
      .catch((error) => {
        EventBus.$emit('failedAuthentication', error);
      });
  },
};

const mutations = {
  // isolated data mutations
  setBuildingsMap(state, data) {
    state.buildingsMap = data;
  },
  setUserData(state, payload) {
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    localStorage.token = payload.jwt.token;
    state.jwt = payload.jwt;
  },
};

const getters = {
  // reusable data accessors
  isAuthenticated(state) {
    return isValidJwt(state.jwt.token);
  },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
