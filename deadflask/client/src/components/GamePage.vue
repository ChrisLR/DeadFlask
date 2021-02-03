<template>
  <div class="container">
    <div class="row">
      <div class="col"><CharacterMap /></div>
      <div class="col"><CharacterLook /></div>
    </div>
    <div class="row">
      <div class="col"><CharacterInfo /></div>
      <div class="col"></div>
    </div>
  </div>
</template>

<script>

import CharacterInfo from './CharacterInfo.vue';
import CharacterMap from './CharacterMap.vue';
import CharacterLook from './CharacterLook.vue';

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
    CharacterLook,
  },
  methods: {},
  beforeMount() {
    this.$store.dispatch('loadCharacterInfo');
  },
};
</script>
