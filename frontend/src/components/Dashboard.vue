<template>
    <div id="loaderHolder" v-if="loading">
        <LoadingScreen />
    </div>
        <div v-else>
            <div>
            <div class="text-3xl my-4 md:my-8">{{ yFinanceData['fullName'] || '&nbsp;'}}</div>
            <form class="max-w-xs mx-auto" @submit="handleSubmit">   
                <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                        </svg>
                    </div>
                    <input 
                        type="search" 
                        @keydown="handleKeyDown"
                        @keydown.enter.prevent="handleSubmit" 
                        v-model="stock" id="default-search" 
                        class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                        placeholder="Stock Name" 
                        required
                        >
                    <button type="submit" class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
                </div>
            </form>
        </div>
        <div class="md:columns-2 p-4 md:px-16 2xl:px-64">
            <div class="chart mx-auto md:p-8">
                <Line
                    id="operating-cash-flow"
                    label="Operating Cash Flow"
                    :data="prepareChartData('operatingCashFlow', 'Operating Cash Flow', 'operatingCashFlowTTM')"
                    
                />
                <Line
                    class="my-4 md:mt-8"
                    id="free-cash-flow"
                    label="Free Cash Flow"
                    :data="prepareChartData('freeCashFlow', 'Free Cash Flow', 'freeCashFlowTTM')"
                />
            </div>
            <div class="chart mx-auto md:p-8">
                <Line
                    id="net-income"
                    label="Net Income"
                    :data="prepareChartData('netIncomeFromContinuingOperations', 'Net Income', 'netIncomeFromContinuingOperationsTTM')"
                />
                <Line
                    class="my-4 md:mt-8"
                    id="total-revenue"
                    label="Total Revenue"
                    :data="prepareChartData('totalRevenue', 'Total Revenue', 'incomeStatementTTM')"
                />
            </div>
        </div>
        <Finviz />
    </div>

</template>
<script>
import Finviz from './Finviz.vue'
import LoadingScreen from './LoadingScreen.vue'
import { Chart, registerables } from 'chart.js'
import { Line } from 'vue-chartjs'
import { mapGetters, mapActions } from 'vuex';
import moment from 'moment'
Chart.register(...registerables);

export default {
    name: 'Dashboard',
    components: {
        Line,
        Finviz,
        LoadingScreen 
    },
    data(){
        return {
            stock: "AAPL",
            chartOptions: {
                responsive: true,
                // maintainAspectRatio: false
            }
        }
    },
    async mounted(){
        await this.getYFinanceData();
    },
    computed: {
        ...mapGetters(['yFinanceData', 'loading']),
        prepareChartData() {
            let timestamps;
            let values;
            return (dataKey, label, ttmKey) => {
                if (this.yFinanceData[dataKey]) {
                    timestamps = Object.keys(this.yFinanceData[dataKey]).map(Number);
                    values = Object.values(this.yFinanceData[dataKey]).map(Number);
                    timestamps = timestamps.map((timestamp) => moment(timestamp).format('DD/MM/YY'));
                    timestamps.push('TTM');
                    values.push(this.yFinanceData[ttmKey]);
                }

                return {
                    labels: timestamps,
                    datasets: [{ label, data: values }],
                };
            }
        },
    },
    methods: {
        ...mapActions(['getYFinanceData', 'getFinvizData']),
        async handleSubmit(event) {
            event.preventDefault();
            await this.getYFinanceData(this.stock);
            await this.getFinvizData(this.stock);
        },
        handleKeyDown(event) {
            if (event.key === 'Backspace') {
                this.stock = '';
                event.preventDefault();
            }
        }
    }
}
</script>
<style>
#loaderHolder{
    min-height: 100vh;
    color: #ADAFB6;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(249, 251, 255,0.6);  
}
</style>