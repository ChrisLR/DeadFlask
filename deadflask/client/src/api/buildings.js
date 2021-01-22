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
    fetchBuildingsMap() {
      const path = `${srvPath}/map`;
      axios.get(path, axiosConfig)
        .then((res) => {
          return res.data;
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
