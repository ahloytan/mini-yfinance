<template>
    <LoadingScreen v-if="isLoading"/>
    <SearchBar />
    <div class="md:columns-2 p-4 md:px-16 2xl:px-64">
        <div class="chart mx-auto md:p-8">
            <Line
                id="operating-cash-flow"
                label="Operating Cash Flow"
                :data="prepareChartData('operatingCashFlow', 'Operating Cash Flow', 'operatingCashFlowTTM', 'rgba(255, 159, 64, 1)')"
                
            />
            <Line
                class="my-4 md:mt-8"
                id="free-cash-flow"
                label="Free Cash Flow"
                :data="prepareChartData('freeCashFlow', 'Free Cash Flow', 'freeCashFlowTTM', 'rgba(75, 192, 192, 1)')"
            />
        </div>
        <div class="chart mx-auto md:p-8">
            <Line
                id="net-income"
                label="Net Income"
                :data="prepareChartData('netIncomeFromContinuingOperations', 'Net Income', 'netIncomeFromContinuingOperationsTTM', 'rgba(54, 162, 235, 1)')"
            />
            <Line
                class="my-4 md:mt-8"
                id="total-revenue"
                label="Total Revenue"
                :data="prepareChartData('totalRevenue', 'Total Revenue', 'incomeStatementTTM', 'rgba(153, 102, 255, 1)')"
            />
        </div>
    </div>
    <div ref="lazyLoadTarget">
        <Finviz v-if="isInView"/>
    </div>
</template>
<script>
import Finviz from './Finviz.vue'
import SearchBar from './SearchBar.vue'
import LoadingScreen from './LoadingScreen.vue'
import { Chart, registerables } from 'chart.js'
import { Line } from 'vue-chartjs'
import { mapGetters, mapActions } from 'vuex';
import dayjs from 'dayjs'
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
            },
            isInView: false,
        }
    },
    async created(){
        await this.getYFinanceData();
    },
    computed: {
        ...mapGetters(['yFinanceData', 'isLoading']),
        prepareChartData() {
            let timestamps;
            let values;
            return (dataKey, label, ttmKey, color) => {
                if (this.yFinanceData[dataKey]) {
                    timestamps = Object.keys(this.yFinanceData[dataKey]);
                    values = Object.values(this.yFinanceData[dataKey]);
                    timestamps = timestamps.map((timestamp) => dayjs(timestamp).format('DD/MM/YY'));
                    timestamps.push('TTM');
                    values.push(this.yFinanceData[ttmKey]);
                }

                return {
                    labels: timestamps,
                    datasets: [{ label, data: values, borderColor: color, backgroundColor: color,}]
                };
            }
        },
    },
    methods: {
        ...mapActions(['getYFinanceData', 'getFinvizData']),
    },
    mounted() {
        const observer = new IntersectionObserver(([entry]) => {
                if (entry.isIntersecting) {
                    this.isInView = true;
                    observer.disconnect(); // Stop observing after loading
                }
            },
            { threshold: 0.1 });

        const target = this.$refs.lazyLoadTarget;
        if (target) observer.observe(target);
    },
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