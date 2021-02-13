<template>
  <div>
    <div v-for="(action, ai) in actions" :key="ai">
      <b-button v-on:click="doAction(action, ai)">
        {{ action.name }}
      </b-button>
      <b-input v-model="freeFormTexts[ai]" v-if="action.requires_freeform_text"/>
    </div>
  </div>
</template>

<script>

import { mapState } from 'vuex';

export default {
  data() {
    return {
      freeFormTexts: [],
    };
  },
  name: 'CharacterActions',
  computed: mapState({
    actions: (state) => state.characterActions,
  }),
  methods: {
    doAction(action, ai) {
      // eslint-disable-next-line no-debugger
      this.$store.dispatch(
        'doCharacterAction',
        { name: action.name, freeform_text: this.$data.freeFormTexts[ai] },
      );
      this.$data.freeFormTexts = [];
    },
  },
  beforeMount() {
    this.$store.dispatch('loadCharacterActions');
  },
};
</script>
