<template>
  <div class="container">
    <div class="row">
      <div>
        <table class="table">
          Hello
          <tbody>
            <tr v-for="(row, ri) in buildings" :key="ri">
              <td v-for="(building, bi) in row" :key="bi">
                <button type="button">{{ building.name }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
      const path = 'http://localhost:5000/map';
      axios.get(path)
        .then((res) => {
          this.buildings = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
        });
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
