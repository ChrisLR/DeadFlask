<template>
  <div class="container">
  <div class="row">
    <CharacterMap />
  </div>
  <div class="row">
    <CharacterInfo />
  </div>
</div>
</template>

<script>

import CharacterInfo from './CharacterInfo.vue';
import CharacterMap from './CharacterMap.vue';

export default {
  data() {
    return {
      name: '',
      health: 0,
      experience: 0,
      is_zombie: false,
    };
  },
  name: 'CharacterPage',
  components: {
    CharacterInfo,
    CharacterMap,
  },
  methods: {},
  beforeMount() {
    this.$store.dispatch('loadCharacterInfo');
  },
};
</script>
