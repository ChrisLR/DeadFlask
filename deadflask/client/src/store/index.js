/* eslint-disable no-shadow */
import Vue from 'vue';
import Vuex from 'vuex';
import { fetchBuildingsMap, moveTo } from '../api/index';

Vue.use(Vuex);

const state = {
  // single source of data
  buildingsMap: [],
};

const actions = {
  // asynchronous operations
  loadBuildingsMap(context) {
    return fetchBuildingsMap().then((response) => context.commit('setBuildingsMap', response.data));
  },
  moveToBuilding(context, { buildingId }) {
    return moveTo(buildingId).then((response) => context.commit('setBuildingsMap', response.data));
  },
};

const mutations = {
  // isolated data mutations
  setBuildingsMap(state, data) {
    state.buildingsMap = data;
  },
};

const getters = {
  // reusable data accessors
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
