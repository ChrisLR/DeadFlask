<template>
  <div>
    <div v-for="character in characters" v-bind:key="character.id">
      <button type="button" v-on:click="logCharacter(character.id)">{{character.name}}</button>
      <br>
    </div>
  </div>
</template>

<script>
import { fetchCharacters } from '../api/index';

export default {
  data() {
    return {
      characters: [],
    };
  },
  name: 'CreateCharacter',
  methods: {
    logCharacter(characterId) {
      this.$store.commit('setCharacterId', characterId);
      this.$router.push('/');
    },
  },
  beforeMount() {
    fetchCharacters().then(
      (response) => { this.characters = response.data.characters; },
    );
  },
};
</script>
