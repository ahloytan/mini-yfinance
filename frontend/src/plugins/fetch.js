'use strict';

import axios from 'axios';

let axiosConfig = {
  baseURL: import.meta.env.VITE_BASE_URL === 'prod' ? import.meta.env.VITE_ENDPOINT: 'http://localhost:5000/',
};

let axiosAgent = axios.create(axiosConfig);

async function fetch(config) {
  let result = await axiosAgent(config);
  return result;
}

export { fetch };
export default {
  install(Vue) {
    Vue.prototype.$fetch = fetch;
  },
};
