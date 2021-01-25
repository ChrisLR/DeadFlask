import Vue from 'vue';
import Router from 'vue-router';
import Buildings from '../components/Buildings.vue';
import Login from '../components/Login.vue';
import store from '../store/index';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/map',
      name: 'Buildings',
      component: Buildings,
      beforeEnter(to, from, next) {
        if (!store.getters.isAuthenticated) {
          next('/login');
        } else {
          next();
        }
      },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
  ],
});
