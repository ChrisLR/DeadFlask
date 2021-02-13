<template>
  <div>
    <div v-for="(log, li) in logs" :key="li">
      {{ log.message }} <br>
    </div>
  </div>
</template>

<script>

import { mapState } from 'vuex';

export default {
  name: 'CharacterLogs',
  computed: mapState({
    logs: (state) => state.characterLogs,
  }),
  methods: {},
  beforeMount() {
    this.$store.dispatch('loadCharacterLogs');
  },
};
</script>
