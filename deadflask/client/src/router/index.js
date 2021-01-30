import Vue from 'vue';
import Router from 'vue-router';
import CharacterMap from '../components/CharacterMap.vue';
import Login from '../components/Login.vue';
import CreateCharacter from '../components/CreateCharacter.vue';
import GamePage from '../components/GamePage.vue';
import LogCharacter from '../components/LogCharacter.vue';
import store from '../store';

Vue.use(Router);

// This ensures the store is properly initialized BEFORE accessing an Url
// Otherwise the token is not loaded when routing and the guard fails
store.commit('initialiseStore');

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/map',
      name: 'CharacterMap',
      component: CharacterMap,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/log_character',
      name: 'LogCharacter',
      component: LogCharacter,
    },
    {
      path: '/create_character',
      name: 'CreateCharacter',
      component: CreateCharacter,
    },
    {
      path: '/',
      name: 'GamePage',
      component: GamePage,
    },
  ],
});

router.beforeResolve((to, from, next) => {
  if (to.path !== '/login' && !store.getters.isAuthenticated) {
    next({ name: 'Login' });
  } else if (to.path !== '/log_character' && store.getters.isAuthenticated && !store.getters.hasChosenCharacter) {
    next({ name: 'LogCharacter' });
  } else {
    next();
  }
});

export default router;
