<template>
<div class="relative overflow-x-auto">
    <table class="w-full text-sm md:text-base text-center text-gray-500 dark:text-gray-400">
        <thead class="text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="px-6 py-3">
                    Field
                </th>
                <th scope="col" class="px-6 py-3">
                    Value
                </th>
                <th scope="col" class="px-6 py-3">
                    Pass/Fail
                </th>
            </tr>
        </thead>
        <tbody class="">
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">PEG</th>
                <td :class="['px-6', 'py-4', pegCalculation ? 'text-green-500' : 'text-red-500']">
                    {{ finvizData['peg'] || 'ERROR' }}
                </td>
                <td v-if="pegCalculation" class="px-6 py-4 text-green-500">Pass (Ideally &lt;=3) </td>
                <td v-else class="px-6 py-4 text-red-500">Fail (Ideally &lt;=3) </td>
            </tr>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">Current Ratio</th>
                <td :class="['px-6', 'py-4', currentRatioCalculation ? 'text-green-500' : 'text-red-500']">
                    {{ finvizData['currentRatio'] || 'ERROR' }}
                </td>
                <td v-if="currentRatioCalculation" class="px-6 py-4 text-green-500">Pass (Ideally &gt;=1) </td>
                <td v-else class="px-6 py-4 text-red-500">Fail (Ideally &gt;=1) </td>
            </tr>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">ROE</th>
                <td class="px-6 py-4">{{ finvizData['roe'] || 'ERROR' }}</td>
                <td class="px-6 py-4">NIL</td>
            </tr>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">EPS Next 5 Years</th>
                <td class="px-6 py-4">{{ finvizData['epsNext5Y'] || 'ERROR' }}</td>
                <td class="px-6 py-4">NIL</td>
            </tr>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">Beta</th>
                <td class="px-6 py-4">{{ finvizData['beta'] || 'ERROR' }}</td>
                <td class="px-6 py-4">NIL</td>
            </tr>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">SHS Outstanding</th>
                <td class="px-6 py-4">{{ finvizData['shsOutstanding'] || 'ERROR' }}</td>
                <td class="px-6 py-4">NIL</td>
            </tr>
        </tbody>
    </table>
</div>

</template>
<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    name: 'Finviz',
    async created(){

        try {
            await this.getFinvizData();
            this.$toast.success(this.$toastMsg.SUCCESS);
            
        } catch (error) {
            this.$toast.success(this.$toastMsg.ERROR);
        }
    },
    computed: {
        ...mapGetters(['finvizData']),
        pegCalculation(){
            return this.finvizData['peg'] <= 3;
        },
        currentRatioCalculation() {
            return this.finvizData['currentRatio'] >= 1 ? 'Pass' : 'Fail';
        },     
    },
    methods: {
        ...mapActions(['getFinvizData']),
    }
}
</script>