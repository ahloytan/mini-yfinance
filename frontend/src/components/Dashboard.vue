<template>
    <LoadingScreen v-if="loading"/>
    <SearchBar />
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
</template>
<script>
import Finviz from './Finviz.vue'
import SearchBar from './SearchBar.vue'
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
        SearchBar,
        LoadingScreen 
    },
    data(){
        return {
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