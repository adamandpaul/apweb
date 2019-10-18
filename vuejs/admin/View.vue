<template>
    <div>
        <v-lazy>
            <div v-if="error">{{ error }}</div>
            <div v-else-if="loading">Loading...</div>
            <div v-else>
                <component :is="view.ui" :data="data" />
            </div>
        </v-lazy>
    </div>
</template>
<script>

import {mapGetters} from 'vuex'
import {resolve} from 'url'

export default {

    props: {
        viewName: String,
    },

    data() {
        return {
            error: null,
            loading: true,
            data: null,
        }
    },

    computed: {
        ...mapGetters([
            'viewsByName',
            'resourceApi',
        ]),
        view() {
            return this.viewsByName[this.viewName]
        },
    },

    methods: {
        load() {
            this.error = null
            this.loading = true
            this.data = null
            if (this.view.api === null) {
                this.loading = false
                return
            }
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
