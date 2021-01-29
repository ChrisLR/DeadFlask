<template>
  <div class="container">
    <table class="table table-bordered" style="empty-cells: show;table-layout: fixed;width: 50%;">
      <tr v-for="(row, ri) in buildingsMap" :key="ri">
       <td v-bind:class="getBuildingStyle(building)" v-for="(building, bi) in row" :key="bi" >
          <div v-if="building" >
            <button type="button" v-on:click="moveTo(building.id)">
              {{ building.name }}
            </button>
          </div>
          <div v-else>
            !
          </div>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'CharacterMap',
  computed: mapState({
    buildingsMap: (state) => state.buildingsMap,
  }),
  methods: {
    getBuildingStyle(building) {
      if (building != null) {
        return `col- ${building.type.replace(' ', '_')}`;
      }
      return 'col-';
    },
    moveTo(buildingId) {
      this.$store.dispatch('moveToBuilding', { buildingId: parseInt(buildingId, 10) });
    },
  },
  beforeMount() {
    this.$store.dispatch('loadBuildingsMap');
  },
};
</script>
