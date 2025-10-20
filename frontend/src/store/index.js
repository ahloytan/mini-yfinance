import { createStore } from 'vuex';
import { fetch } from '../plugins/fetch';

const DEFAULT_STOCK = 'AAPL';
const DEFAULT_VALUE = 'Loading...'

const store = createStore({
  state () {
    return {
      yFinanceData: {},
      finvizData: {
        "beta": DEFAULT_VALUE,
        "currentRatio": DEFAULT_VALUE,
        "epsNext5Y": DEFAULT_VALUE,
        "peg": DEFAULT_VALUE,
        "roe": DEFAULT_VALUE,
        "shsOutstanding": DEFAULT_VALUE
      },
      searchSuggestionsData: [],
      isLoading: false
    }
  },
  getters: {
    yFinanceData: state => state.yFinanceData,
    finvizData: state => state.finvizData,
    searchSuggestionsData: state => state.searchSuggestionsData,
    isLoading: state => state.isLoading
  },
  mutations: {
    setYFinanceData(state, yFinanceData) {
      state.yFinanceData = yFinanceData;
    },
    setFinvizData(state, finvizData) {
      state.finvizData = finvizData;
    },
    setSearchSuggestionsData(state, searchSuggestionsData) {
      state.searchSuggestionsData = searchSuggestionsData;
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
      } catch (error) {
        const {response: { data }} = error;
        throw data.error;

      } finally {

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
        commit('setFinvizData', {});
        throw "No finviz data for this ticker";
      }
    },
    async getSearchSuggestions({commit}, stock) {
      try {
        const {data: {data}} = await fetch({
          method: 'GET',
          url: `search`,
          params: { 
            query: stock
          }
        })

        commit('setSearchSuggestionsData', data);        

      } catch (error) {
        const {response: { data }} = error;
        throw data.error;
      }
    }
  }
})

export default store;