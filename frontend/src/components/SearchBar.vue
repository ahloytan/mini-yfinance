<template>
    <div class="text-3xl my-4 md:my-8">{{ yFinanceData['fullName'] || 'Loading...'}}</div>
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
                @keydown.enter.prevent="handleSubmit" 
                @keydown.backspace.prevent="clearInput"
                v-model="stock" id="default-search" 
                class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                placeholder="Enter Stock Name" 
                autocomplete="off"
                required
            >
            <button type="submit" class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
            <!-- Dropdown -->
            <div 
                v-if="isDropdownVisible && searchSuggestionsData?.length > 0" 
                class="absolute z-10 w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-xl max-h-80 overflow-y-auto"
            >
                <ul class="py-2">
                    <li 
                        v-for="(item, index) in searchSuggestionsData" 
                        :key="index"
                        @mousedown.prevent="selectStock(item)"
                        class="px-4 py-3 hover:bg-blue-50 dark:hover:bg-gray-700 cursor-pointer transition-colors duration-150 border-b border-gray-100 dark:border-gray-700 last:border-b-0"
                    >
                        <div class="flex items-start justify-between gap-3">
                            <div class="flex-1 min-w-0">
                                <div class="flex items-center gap-2 mb-1">
                                    <span class="font-bold text-sm text-gray-900 dark:text-white">
                                        {{ item.symbol }}
                                    </span>
                                    <span class="text-xs px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                                        {{ item.exchDisp }}
                                    </span>
                                </div>
                                <div class="text-left text-sm text-gray-700 dark:text-gray-300 truncate font-medium mb-1">
                                    {{ item.longname || item.shortname }}
                                </div>
                                <div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                                    <span>{{ item.typeDisp }}</span>
                                    <span v-if="item.industryDisp" class="before:content-['•'] before:mr-2">
                                        {{ item.industryDisp }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </form>
    <span class="text-xs text-gray-500">*figures are all in USD (millions)</span>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import { debounce } from 'lodash';

export default {
    name: 'SearchBar',
    data() {
        return {
            stock: "AAPL",
            isDropdownVisible: false
        }
    },
    created() {
        this.debouncedSearch = debounce(this.handleKeyDown, 500);
    },
    watch: {
        stock(newVal) {
            this.debouncedSearch(newVal)
        }
    },  
    computed: {
        ...mapGetters(['yFinanceData', 'searchSuggestionsData'])
    },
    methods: {
        ...mapActions(['getYFinanceData', 'getFinvizData', 'getSearchSuggestions']),
        async handleSubmit() {

            try {
                await this.getYFinanceData(this.stock);
                await this.getFinvizData(this.stock);
                this.$toast.success(this.$toastMsg.SUCCESS);
                
            } catch (error) {
                this.$toast.error(error || this.$toastMsg.TICKER_NOT_FOUND);

            } finally {
                this.isDropdownVisible = false;
            }
        },
        async handleKeyDown(value) {
            if (!value) {
                this.isDropdownVisible = false;
                return;
            }

            try {
                await this.getSearchSuggestions(value);
                this.isDropdownVisible = true;

            } catch (error) {
                console.log(error)
            }
        },
        async selectStock(item) {
            this.stock = item.symbol;
            this.handleSubmit();
        },
        clearInput(event) {
            this.stock = '';
            event.preventDefault();
            return;
        }
    }
}
</script>