<template>
  <div>
    {{ description }}
  </div>
</template>

<script>

import { mapState } from 'vuex';

export default {
  name: 'CharacterLook',
  computed: mapState({
    name: (state) => state.building.name,
    description: (state) => state.building.description,
    humans: (state) => state.building.humans,
    zombies: (state) => state.building.zombies,
    corpses: (state) => state.building.corpses,
    is_inside: (state) => state.character.is_inside,
  }),
  methods: {},
};
</script>
