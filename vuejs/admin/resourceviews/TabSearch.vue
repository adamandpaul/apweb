<template>
    <div>
        <v-form ref="form" v-model="valid" @submit.prevent="search">
            <v-card>
                <v-card-title>Search</v-card-title>
                <v-card-text>
                    <v-jsonschema-form v-if="schema" :schema="schema" :model="query" :options="options"/>
                    <v-alert v-if="error" type="error" text>
                        {{ error }}
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="clear">Clear Form</v-btn>
                    <v-btn :loading="inProgress" color="primary" @click="search">Search</v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
        <SearchResults :query="currentQuery" api="@@admin-search" />
    </div>
</template>
<script>

import SearchResults from './SearchResults.vue'

export default {

    components: {
        SearchResults,
    },

    props: {
        data: Object,
    },

    data() {
        return {
            valid: false,
            schema: this.data,
            options: {
                debug: false,
                disableAll: false,
                autoFoldObjects: false,
            },
            error: null,
            query: {},
            currentQuery: null,
        }
    },

    methods: {
        search() {
            if (!this.valid) {
                this.error = "The form did not validate, please check the fields above"
                return
            }
            this.error = null
            this.currentQuery = {...this.query}
        },
        clear() {
            for (let key in this.query) {
                this.query[key] = null
            }
            this.error = null
            this.$refs.form.reset()
        },
    },
}

</script>
