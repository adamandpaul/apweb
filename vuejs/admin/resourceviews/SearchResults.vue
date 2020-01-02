<template>
    <div class="search-results">
        <p class="total" v-if="total">
            Total: {{ total }} item(s)
        </p>
        <div v-for="(page, pageIdx) in pages" :key="pageIdx">
            <hr v-if="pageIdx > 0"/>
            <div class="item" v-for="(item, itemIdx) in page" :key="itemIdx">
                <component :is="item.ui || 'resource-tile'" :tile="item" />
            </div>
        </div>
        <v-progress-linear v-if="inProgress" indeterminate/>
        <v-btn v-if="isMore && !inProgress" @click="more">More</v-btn>
        <template v-if="error">
            <request-error :error="error" />
        </template>
    </div>
</template>
<script>

import {mapGetters} from 'vuex'

const DEFAULT_PAGE_LIMIT = 100

export default {

    props: {
        query: [Object, null],
        api: String,
    },

    data() {
        return {
            limit: DEFAULT_PAGE_LIMIT,
            searchCount: 0,
            total: null,
            pages: [],
            error: null,
            inProgress: false,
        }
    },

    computed: {
        ...mapGetters([
            'resourceApi',
        ]),
        isMore() {
            if (!this.total) {
                return false
            }
            const potentialItems = this.pages.length * this.limit
            return potentialItems < this.total
        },
    },

    watch: {
        query(to) {
            if (to !== null) {
                this.clear()
                this.nextPage(to)
            }
        },
    },

    methods: {

        clear() {
            this.searchCount += 1
            this.total = null
            this.pages = []
            this.error = null
        },

        nextPage(q) {
            const query = q || this.query
            const pageIdx = this.pages.length
            const offset = pageIdx * this.limit
            const params = {
                ...query,
                offset: offset,
                limit: this.limit,
            }
            const xSearchCount = this.searchCount
            this.inProgress = true
            this.error = null
            this.resourceApi.get(this.api, {params, xSearchCount})
                .then(this.handleResponse)
                .catch(this.handleError)
        },

        more() {
            this.nextPage()
        },

        handleResponse(resp) {
            // Check if we are still relavant
            if (resp.config.xSearchCount == this.searchCount) {
                this.inProgress = false
                const results = resp.data.data
                this.pages.push(results.items)
                this.total = results.total
            }
        },

        handleError(err) {
            this.error = err
            this.inProgress = false
        },

    },

    mounted() {
        if (this.query) {
            this.clear()
            this.nextPage()
        }
    },
}


</script>
<style lang="sass" scoped>
.total
    margin: 16px 0

hr
    margin: 16px 0

.item
    margin-bottom: 16px

</style>
