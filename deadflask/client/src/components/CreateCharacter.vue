<template>
  <div>
    <label for="name"></label>
    <input v-model="name" id="name"/>
    <div v-for="character_type in character_types" v-bind:key="character_type.id">
      <input v-model="picked" type="radio"
             :id="'type_' + character_type.id" :value="character_type.id"/>
      <label :for="'type_' + character_type.id">{{ character_type.name }}</label>
      <br>
    </div>
    <button type="button" v-on:click="submitCharacter(picked)">Submit</button>
  </div>
</template>

<script>
import { createCharacter, getCharacterTypes } from '../api/index';

export default {
  data() {
    return {
      picked: '',
      name: '',
      character_types: [],
    };
  },
  name: 'CreateCharacter',
  methods: {
    submitCharacter(characterTypeId) {
      createCharacter({ name: this.name, character_type_id: characterTypeId })
        .then((response) => this.$store.commit('setCharacterId', response.data.characterId))
        .then(() => this.$router.push('/'));
    },
  },
  beforeMount() {
    getCharacterTypes().then(
      (response) => { this.character_types = response.data.character_types; },
    );
  },
};
</script>
