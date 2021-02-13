<template>
  <div>
    <b>Actions</b>
    <div>
      <div v-for="(action, ai) in actions" :key="ai">
        <b-button v-on:click="doAction(action, ai)">
          {{ action.name }}
          <b-input v-model="freeFormTexts[ai]"
                   v-if="action.requires_freeform_text" v-on:click.stop />
        </b-button>

      </div>
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
