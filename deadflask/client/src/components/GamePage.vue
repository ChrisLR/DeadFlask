<template>
  <div class="container">
    <div class="row">
      <div class="col"><CharacterMap/><CharacterInfo/></div>
      <div class="col">
        <CharacterLook/>
        <CharacterLogs/>
        <CharacterActions/>
      </div>
    </div>
  </div>
</template>

<script>

import CharacterInfo from './CharacterInfo.vue';
import CharacterMap from './CharacterMap.vue';
import CharacterLook from './CharacterLook.vue';
import CharacterActions from './CharacterActions.vue';
import CharacterLogs from './CharacterLogs.vue';

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
    CharacterActions,
    CharacterLogs,
  },
  methods: {},
  beforeMount() {
    this.$store.dispatch('loadCharacterInfo');
  },
};
</script>
