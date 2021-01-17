import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/ping.vue';
import Books from '../components/Books.vue';
import Buildings from '../components/Buildings.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    }, {
      path: '/',
      name: 'Books',
      component: Books,
    },
    {
      path: '/map',
      name: 'Buildings',
      component: Buildings,
    },
  ],
});
