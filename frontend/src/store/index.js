import { createStore } from 'vuex';
import { fetch } from '../plugins/fetch';

const DEFAULT_STOCK = 'AAPL';

const store = createStore({
  state () {
    return {
      yFinanceData: {},
      finvizData: {},
      isLoading: false
    }
  },
  getters: {
    yFinanceData: state => state.yFinanceData,
    finvizData: state => state.finvizData,
    isLoading: state => state.isLoading
  },
  mutations: {
    setYFinanceData(state, yFinanceData) {
      state.yFinanceData = yFinanceData;
    },
    setFinvizData(state, finvizData) {
      state.finvizData = finvizData;
    },
    setLoadingStatus(state, status) {
      state.isLoading = status;
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
            stock: stock || DEFAULT_STOCK
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
            stock: stock || DEFAULT_STOCK
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