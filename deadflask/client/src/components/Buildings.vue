<template>
  <div class="container">
    <table class="table table-bordered" style="empty-cells: show;table-layout: fixed;width: 50%;">
      <tr v-for="(row, ri) in buildings" :key="ri">
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
import axios from 'axios';

const srvPath = 'http://localhost:5000';
const axiosConfig = {
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
    'Access-Control-Allow-Origin': 'http://localhost:5000',
  },
};

export default {
  data() {
    return {
      buildings: [],
      message: '',
      showMessage: false,
    };
  },
  components: {},
  methods: {
    getBuildings() {
      const path = `${srvPath}/map`;
      axios.get(path)
        .then((res) => {
          this.buildings = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
        });
    },
    moveTo(buildingId) {
      const path = `${srvPath}/move_to`;
      axios.post(path, { building_id: buildingId }, axiosConfig).then((res) => {
        this.buildings = res.data;
      });
    },
    getBuildingStyle(building) {
      if (building != null) {
        return `col- ${building.type.replace(' ', '_')}`;
      }
      return 'col-';
    },
    initForm() { this.getBuildings(); },
    onSubmit() {},
    onReset() {},
  },
  created() {
    this.getBuildings();
  },
};
</script>
