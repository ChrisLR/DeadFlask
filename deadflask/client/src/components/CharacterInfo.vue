<template>
  <div>
    You are <b>{{ name }}</b> and you are
    <b v-if="is_zombie">dead</b>
    <b v-else>alive</b>
    <br/>
    You have <b>{{ health }}</b> health and <b>{{ experience }}</b> experience.
  </div>
</template>

<script>

import { mapState } from 'vuex';

export default {
  name: 'CharacterInfo',
  computed: mapState({
    health: (state) => state.character.health,
    name: (state) => state.character.name,
    experience: (state) => state.character.experience,
    is_zombie: (state) => state.character.is_zombie,
  }),
  methods: {},
};
</script>
