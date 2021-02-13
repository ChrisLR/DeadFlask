/* eslint-disable no-shadow */
import Vue from 'vue';
import Vuex from 'vuex';
import { isValidJwt, EventBus } from '../utils';
import {
  fetchCharacterMap, moveTo, authenticate, fetchCharacterInfo, fetchCharacterLook,
  fetchCharacterActions, postExecuteAction, fetchCharacterLogs,
} from '../api/index';

Vue.use(Vuex);

const state = {
  // single source of data
  characterActions: {},
  characterLogs: [],
  building: {},
  buildingId: -1,
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
    return fetchCharacterMap(context.state.characterId)
      .then((response) => context.commit('setBuildingsMap', response.data))
      .then(() => context.dispatch('loadCharacterLook'));
  },
  moveToBuilding(context, { buildingId }) {
    return moveTo(buildingId, context.state.characterId)
      .then((response) => context.commit('setBuildingsMap', response.data))
      .then(() => context.commit('setBuildingId', buildingId))
      .then(() => context.dispatch('loadCharacterLook'));
  },
  doCharacterAction(context, action) {
    return postExecuteAction(context.state.characterId, action);
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
  loadCharacterLook(context) {
    return fetchCharacterLook(context.state.characterId)
      .then((response) => context.commit('setBuildingInfo', response.data));
  },
  loadCharacterActions(context) {
    fetchCharacterActions(context.state.characterId)
      .then((response) => context.commit('setCharacterActions', response.data));
  },
  loadCharacterLogs(context) {
    fetchCharacterLogs(context.state.characterId)
      .then((response) => context.commit('setCharacterLogs', response.data));
  },
};

const mutations = {
  setBuildingId(state, data) {
    state.buildingId = data;
  },
  setBuildingInfo(state, data) {
    state.building = data;
  },
  setBuildingsMap(state, data) {
    state.buildingsMap = data.rows;
    state.buildingId = data.building_id;
  },
  setCharacterActions(state, data) {
    state.characterActions = data;
  },
  setCharacterInfo(state, data) {
    state.character = data;
  },
  setCharacterLogs(state, data) {
    console.log(`Doing this ${Object.values(data)}`);
    console.log(`Doing this ${Object.values(data.logs)}`);
    state.characterLogs = data.logs;
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
