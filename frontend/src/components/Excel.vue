<template>
    <LoadingScreen v-if="isLoading"/>
    <div class="md:h-screen">
        <SearchBar />
        <div class="md:flex items-center justify-center">
            <div class="p-4">
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="countries" class="w-full text-left">Select Option:</label>
                    <select id="countries" v-model="valuationMethod" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5">
                        <option :value="yFinanceData['operatingCashFlowTTM']" selected>Discounted Cash Flow ({{ yFinanceData['operatingCashFlowTTM'] }})</option>
                        <option :value="yFinanceData['netIncomeFromContinuingOperationsTTM']">Discounted Net Income ({{ yFinanceData['netIncomeFromContinuingOperationsTTM'] }})</option>
                        <option :value="yFinanceData['freeCashFlowTTM']">Discounted Free Cash Flow ({{ yFinanceData['freeCashFlowTTM'] }})</option>
                        <option value="0">Enter Value Below</option>
                    </select>
                </div>
                <div v-if="valuationMethod == 0" class="max-w-md flex items-center my-6 mx-auto">
                    <label for="valuationMethod" class="w-full text-left">Enter Valuation:</label>
                    <input v-model="enteredValuation" type="number" id="valuationMethod" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div>
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="totalDebt" class="w-full text-left">Total Debt:</label>
                    <input v-model="totalDebt" type="number" id="totalDebt" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div>
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="cashShortTermInvestments" class="w-full text-left">Cash & Short Term Investments:</label>
                    <input v-model="cashEquivalentAndShortTermInvestments" type="number" id="cashShortTermInvestments" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div>
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="countries" class="w-full text-left">FCF Growth Rate (Yr 1-5):</label>
                    <select id="fcf" v-model="fcf" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5">
                        <option :value="yFinanceData['epsNext5Y']">Yahoo Finance ({{ yFinanceData['epsNext5Y'] }}%)</option>
                        <option :value="finvizData['epsNext5Y']">Finviz ({{ finvizData['epsNext5Y'] }}%)</option>
                        <option :value="averageFCFGrowth">Average ({{ averageFCFGrowth }}%)</option>
                        <option value="-1" selected>Enter Value Below</option>
                    </select>
                </div>
                <div v-if="fcf == -1" class="max-w-md flex items-center my-6 mx-auto">
                    <label for="fcfGrowthRateYr1To5" class="w-full text-left">Enter FCF:</label>
                    <input v-model="freeCashFlowGrowthRateYr1To5" type="number" id="fcfGrowthRateYr1To5" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div>
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="fcfGrowthRateYr6To10" class="w-full text-left">FCF Growth Rate (Yr 6-10):</label>
                    <input v-model="freeCashFlowGrowthRateYr6To10" type="number" id="fcfGrowthRateYr6To10" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div>
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="fcfGrowthRateYr11To20" class="w-full text-left">FCF Growth Rate (Yr 11-20):</label>
                    <input v-model="freeCashFlowGrowthRateYr11To20" type="number" id="fcfGrowthRateYr11To20" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div>
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="discountRate" class="w-full text-left">Discount Rate:</label>
                    <input v-model=discountRate type="number" id="discountRate" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div> 
                <div class="max-w-md flex items-center my-6 mx-auto">
                    <label for="lastClose" class="w-full text-left">Last Close:</label>
                    <input v-model="lastClose" type="number" id="lastClose" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 blockw-max p-2.5" required>
                </div> 
            </div>
            <div class="p-4">
                <table class="text-center mx-auto">
                    <thead class="text-sm md:text-base uppercase bg-gray-50">
                        <tr>
                            <th scope="col" class="px-6 py-3">Field</th>
                            <th scope="col" class="px-6 py-3">Value</th>
                        </tr>
                    </thead>
                    <tbody> 
                        <tr class="bg-white border-b text-left">
                            <th scope="row" class="px-6 py-4 ">No. Of Outstanding Shares</th>
                            <td class="px-6 py-4 ">{{ numOutstandingShares }} millions</td>
                        </tr>
                        <tr class="bg-white border-b text-left">
                            <th scope="row" class="px-6 py-4 ">PV of 20yrs Free Cash Flow</th>
                            <td class="px-6 py-4 ">{{ pv20YrsFreeCashFlow }}</td>
                        </tr>
                        <tr class="bg-white border-b text-left">
                            <th scope="row" class="px-6 py-4 ">Instrinsic Value Before Cash/Debt</th>
                            <td class="px-6 py-4 ">{{ instrinsicValueBeforeCashOrDebt.toFixed(2) }}</td>
                        </tr>
                        <tr class="bg-white border-b text-left">
                            <th scope="row" class="px-6 py-4 ">Less Debt Per Share</th>
                            <td class="px-6 py-4 ">{{ lessDebtPerShare.toFixed(2) }}</td>
                        </tr>
                        <tr class="bg-white border-b text-left">
                            <th scope="row" class="px-6 py-4 ">Plus(+) Cash Per Share</th>
                            <td class="px-6 py-4 ">{{ plusCashPerShare.toFixed(2)  }}</td>
                        </tr>
                        <tr class="bg-teal-200 text-left">
                            <th scope="row" class="px-6 py-4">Instrinsic Value Per Share</th>
                            <td class="px-6 py-4 font-bold">{{ instrinsicValuePerShare.toFixed(2) }}</td>
                        </tr>
                        <tr class="bg-teal-200 text-left">
                            <th scope="row" class="px-6 py-4 ">Discount/Premium</th>
                            <td class="px-6 py-4 font-bold">{{ discountPremium.toFixed(2) }}%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
import LoadingScreen from './LoadingScreen.vue'
import SearchBar from './SearchBar.vue'
import { mapGetters, mapActions } from 'vuex';
export default {
    name: "Excel",
    components: {
        LoadingScreen,
        SearchBar
    },
    data() {
        return {
            fcf: -1,
            base: 4.18,
            lastClose: 140.0,
            totalDebt: 52907,
            discountRate: 5.0,
            valuationMethod: 0,
            enteredValuation: 21410,
            valuationMethodValue: -1,
            freeCashFlowGrowthRateYr1To5: 5.30,
            freeCashFlowGrowthRateYr6To10: 4.18,
            freeCashFlowGrowthRateYr11To20: 4.18,
            cashEquivalentAndShortTermInvestments: 24613
        }
    },
    async mounted(){
        await this.getFinvizData();
        await this.getYFinanceData();
    },
    watch: {
        yFinanceData() {
            const cashEquivalentData = Object.values(this.yFinanceData['cashEquivalentAndShortTermInvestments'])
            this.cashEquivalentAndShortTermInvestments = Math.floor(cashEquivalentData[cashEquivalentData.length - 1]);
            this.valuationMethod = this.yFinanceData['operatingCashFlowTTM'];  
            this.fcf = this.yFinanceData['epsNext5Y'];
            this.totalDebt = Math.floor(Object.values(this.yFinanceData['totalDebt'])[0]);
            this.lastClose = this.yFinanceData['lastClose'];
            this.valuationMethodValue = this.yFinanceData['operatingCashFlowTTM'];
            this.freeCashFlowGrowthRateYr6To10Calculation(this.yFinanceData['epsNext5Y']);
        },
        finvizData() {
            this.discountRate = this.discountRateCalculation(this.finvizData['beta']);
        },
        freeCashFlowGrowthRateYr1To5() {
            this.freeCashFlowGrowthRateYr6To10Calculation(this.yFinanceData['epsNext5Y']);
        }
    },
    computed: {
        ...mapGetters(['yFinanceData', 'finvizData', 'isLoading']),
        numOutstandingShares() {
            const shsOutstanding = this.finvizData['shsOutstanding'];
            const denomination = shsOutstanding ? shsOutstanding.slice(-1) : 0;
            
            if (denomination === 'B') return parseFloat(shsOutstanding.slice(0, -1)) * 1000;
            if (denomination === 'M') return parseFloat(shsOutstanding.slice(0, -1));
            return 1
        },
        pv20YrsFreeCashFlow() {
            let discountedValueTotal = 0;
            let fcfGrowthRateSelectedOrEntered = this.fcf != -1 ? this.fcf : this.freeCashFlowGrowthRateYr1To5;
            let valuationValueSelectedOrEntered = this.valuationMethod == 0 ? this.enteredValuation : this.valuationMethod;
            let projectedFreeCashFlow = valuationValueSelectedOrEntered * (1 + (fcfGrowthRateSelectedOrEntered / 100));
            let discountFactor = 1 / (1 + (this.discountRate / 100));

            discountedValueTotal = projectedFreeCashFlow * discountFactor

            const growthRates = [fcfGrowthRateSelectedOrEntered, this.freeCashFlowGrowthRateYr6To10, this.freeCashFlowGrowthRateYr11To20];

            for (let i = 1; i < 20; i++) {
                let growthRate = growthRates[0];
                if (i >= 5 && i < 10) {
                    growthRate = growthRates[1];
                } else if (i >= 10) {
                    growthRate = growthRates[2];
                }

                projectedFreeCashFlow *= (1 + growthRate / 100);
                discountFactor = discountFactor / (1 + (this.discountRate / 100));
                discountedValueTotal += projectedFreeCashFlow * discountFactor;
            }

            return Math.ceil(discountedValueTotal);
        
        },
        instrinsicValueBeforeCashOrDebt() {
            return this.pv20YrsFreeCashFlow / this.numOutstandingShares;
        },
        lessDebtPerShare() {
            return this.totalDebt / this.numOutstandingShares;
        },
        plusCashPerShare() {
            return this.cashEquivalentAndShortTermInvestments / this.numOutstandingShares;
        },
        instrinsicValuePerShare() {
            return this.instrinsicValueBeforeCashOrDebt - this.lessDebtPerShare + this.plusCashPerShare;
        },
        discountPremium(){
            return (this.lastClose / this.instrinsicValuePerShare - 1) * 100;
        },
        averageFCFGrowth() {
            return (this.yFinanceData['epsNext5Y'] + this.finvizData['epsNext5Y']) / 2
        }
    },
    methods: {
        ...mapActions(['getYFinanceData', 'getFinvizData']),
        discountRateCalculation(betaVal) {
            const beta = betaVal || 0;

            if (beta < 1) return 5.0;
            if (beta < 1.1) return 5.8;
            if (beta < 1.2) return 6.2;
            if (beta < 1.3) return 6.6;
            if (beta < 1.4) return 7.0;
            if (beta < 1.5) return 7.4;
            if (beta <= 1.6) return 7.8;

            return 8.2
        },
        freeCashFlowGrowthRateYr6To10Calculation(epsNext5Y) {
            this.freeCashFlowGrowthRateYr6To10 = epsNext5Y / 2;
            if (this.freeCashFlowGrowthRateYr6To10 <= this.base) this.freeCashFlowGrowthRateYr6To10 = this.base;
            if (this.freeCashFlowGrowthRateYr6To10 >= 15) this.freeCashFlowGrowthRateYr6To10 = 15;
        },
    }
}
</script>
<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}

#fcf {
    max-width: 220px;
}
</style>