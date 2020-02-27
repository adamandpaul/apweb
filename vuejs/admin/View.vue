<template>
    <div class="view">
        <div v-if="error">
            <request-error :error="error" />
        </div>
        <div v-if="reloading">Reloading...</div>
        <div v-if="loading">Loading...</div>
        <div v-else>
            <component v-show="!reloading" :is="view.ui" :data="data" :options="options" :resourceURL="_resourceURL" :resourceApi="resourceApi" />
        </div>
    </div>
</template>
<script>

import {mapGetters} from 'vuex'
import {resolve} from 'url'

export default {

    props: {
        view: Object,
        resourceURL: [String, null],
    },

    data() {
        return {
            error: null,
            loading: true,
            reloading: false,
            data: null,
        }
    },

    computed: {
        _resourceURL() {
            return this.resourceURL || this.$store.getters.resourceURL
        },
        resourceApi() {
            return this.$store.getters.resourceApiForResourceURL(this._resourceURL)
        },
        options() {
            return this.view.options || {}
        }
    },

    methods: {
        load() {
            this.error = null
            this.loading = true
            this.data = null
            if (this.view.api !== "" && !this.view.api) {
                this.loading = false
                return
            }
            this.resourceApi.get(this.view.api)
                .then(this.handleApiResponse)
                .catch(this.handleApiError)
        },
        reload() {
            this.resourceApi.get(this.view.api)
                .then(this.handleApiResponse)
                .catch(this.handleApiError)
        },
        handleApiResponse(resp) {
            this.data = resp.data.data
            this.loading = false
        },
        handleApiError(error) {
            this.error = error
            this.loading = false
        },
    },

    mounted() {
        this.load()
    },

}
</script>
<style lang="sass" scoped>

.view
    margin: 32px 0


</style>
