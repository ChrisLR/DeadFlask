<template>
  <div>
    <section class="hero is-primary">
      <div>
        <div class="container has-text-centered">
          <h2 class="title">Login</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="field">
          <label for="email">Email:</label>
          <div class="control">
            <input type="email" id="email" v-model="email">
          </div>
        </div>
        <div class="field">
          <label for="password">Password:</label>
          <div class="control">
            <input type="password" id="password" v-model="password">
          </div>
        </div>

        <div class="control">
          <a class="button is-large is-primary" @click="authenticate">Login</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { EventBus } from '../utils';

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMsg: '',
    };
  },
  methods: {
    authenticate() {
      this.$store.dispatch('login', { email: this.email, password: this.password })
        .then(() => this.$router.push('/'));
    },
  },
  mounted() {
    EventBus.$on('failedAuthentication', (msg) => {
      this.errorMsg = msg;
    });
  },
  beforeDestroy() {
    EventBus.$off('failedAuthentication');
  },
};
</script>
