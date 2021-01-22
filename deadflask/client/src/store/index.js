/* eslint-disable no-shadow */
import Vue from 'vue';
import Vuex from 'vuex';
import fetchBuildingsMap from '../api/buildings';

Vue.use(Vuex);

const state = {
  // single source of data
  buildingsMap: [],
};

const actions = {
  // asynchronous operations
  loadBuildingsMap(context) {
    return fetchBuildingsMap()
      .then((data) => context.commit('setBuildingsMap', data));
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
