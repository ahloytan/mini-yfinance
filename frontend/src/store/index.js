import { createStore } from 'vuex';
import { fetch } from '../plugins/fetch';

const store = createStore({
  state () {
    return {
      yFinanceData: {},
      finvizData: {},
      loading: false
    }
  },
  getters: {
    yFinanceData: state => state.yFinanceData,
    finvizData: state => state.finvizData,
    loading: state => state.loading
  },
  mutations: {
    setYFinanceData(state, yFinanceData) {
      state.yFinanceData = yFinanceData;
    },
    setFinvizData(state, finvizData) {
      state.finvizData = finvizData;
    },
    setLoadingStatus(state, status) {
      state.loading = status;
    },
  },
  actions: {
    async getYFinanceData({commit}, stock) {
      try {
        commit('setLoadingStatus', true);
        const {data: {data}} = await fetch({
          method: 'GET',
          url: 'yfinance_data',
          params: {
            stock: stock || 'AAPL'
          }
        })
        
        for (const key in data){
          if (key == 'fullName') continue

          if (typeof data[key] === 'string') data[key] = JSON.parse(data[key])
        }

        commit('setYFinanceData', data);
        commit('setLoadingStatus', false);
      } catch (error) {
        console.log(error);
        commit('setLoadingStatus', false);
      }
    },
    async getFinvizData({commit}, stock) {
      try {
        const {data: {data}} = await fetch({
          method: 'GET',
          url: 'finviz_data',
          params: {
            stock: stock || 'AAPL'
          }
        })

        commit('setFinvizData', data);
      } catch (error) {
        console.log(error);
      }
    },
  }
})

export default store;