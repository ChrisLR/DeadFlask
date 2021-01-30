/* eslint-disable no-shadow */
import Vue from 'vue';
import Vuex from 'vuex';
import { isValidJwt, EventBus } from '../utils';
import {
  fetchBuildingsMap, moveTo, authenticate, fetchCharacterInfo,
} from '../api/index';

Vue.use(Vuex);

const state = {
  // single source of data
  buildingsMap: [],
  character: {},
  characterId: -1,
  user: {},
  jwt: '',
  token: '',
};

const actions = {
  // asynchronous operations
  loadBuildingsMap(context) {
    return fetchBuildingsMap(context.state.characterId)
      .then((response) => context.commit('setBuildingsMap', response.data));
  },
  moveToBuilding(context, { buildingId }) {
    return moveTo(buildingId, context.state.characterId)
      .then((response) => context.commit('setBuildingsMap', response.data));
  },
  login(context, userData) {
    context.commit('setUserData', { userData });
    return authenticate(userData)
      .then((response) => context.commit('setJwtToken', { jwt: response.data }))
      .catch((error) => {
        EventBus.$emit('failedAuthentication', error);
      });
  },
  loadCharacterInfo(context) {
    return fetchCharacterInfo(context.state.characterId)
      .then((response) => context.commit('setCharacterInfo', response.data));
  },
};

const mutations = {
  // isolated data mutations
  setBuildingsMap(state, data) {
    state.buildingsMap = data;
  },
  setCharacterInfo(state, data) {
    state.character = data;
  },
  setCharacterId(state, data) {
    state.characterId = data;
    localStorage.setItem('characterId', data);
  },
  setUserData(state, payload) {
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    localStorage.setItem('token', payload.jwt.token);
    state.jwt = payload.jwt;
    state.token = payload.jwt.token;
  },
  initialiseStore(state) {
    const token = localStorage.getItem('token');
    if (token) { state.token = token; }
    const characterId = localStorage.getItem('characterId');
    if (characterId) { state.characterId = characterId; }
  },
};

const getters = {
  // reusable data accessors
  isAuthenticated(state) {
    return isValidJwt(state.token);
  },
  hasChosenCharacter(state) {
    return state.characterId > -1;
  },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
