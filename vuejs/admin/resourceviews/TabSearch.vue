<template>
    <div>        
        <v-form ref="form" v-model="valid" @submit.prevent="search">
            <v-card flat>
                <v-card-title>Search</v-card-title>
                <v-card-text>
                    <v-jsonschema-form v-if="schema_search" :schema="schema_search" :model="query" :options="formOptions"/>
                    <v-alert v-if="error" type="error" text>
                        {{ error }}
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="clear">Clear Form</v-btn>
                    <v-btn color="primary" @click="search">Search</v-btn>
                    <v-btn class="btn-add-new" v-if="schema_add" color="secondary" @click="addNew">Add New Item</v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
        <SearchResults v-if="!showAdd" :query="currentQuery" api="@@admin-search" />
        <div class="add-new-form" v-if="showAdd">
            <v-card>
                <v-card-text>
                    <resource-tab-add :data="schema_add_" :options_add="options_add" :resourceURL="resourceURL" :resourceApi="resourceApi" />
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>
<script>

import SearchResults from './SearchResults.vue'
import {mapGetters} from 'vuex'


export default {

    components: {
        SearchResults,
    },

    props: {
        data: {type: Object, default: null},
        options: {type: Object, default: null},
        resourceURL: {type: String, default: null},
        resourceApi: {type: Function, default: null},
    },

    data() {
        return {
            valid: false,
            formOptions: {
                debug: false,
                disableAll: false,
                autoFoldObjects: false,
            },
            error: null,
            query: {},
            currentQuery: null,
            showAdd: false,
            schema_add_: null,
        }
    },

    computed: {
        schema_search() {
            return this.data["schema_search"] || this.options["schema_search"]
        },
        schema_add() {
            return this.data["schema_add"] || this.options["schema_add"]
        },
        options_add() {
            return this.options.options_add || {}
        },
    },

    watch: {
        schema_add() {
            this.update_schema_add()
            this.schema_add_set_defaults()
        },
        query: {
            handler() {
                this.schema_add_set_defaults()
            },
            deep: true,
        },
    },

    mounted() {
        this.update_schema_add()
        this.schema_add_set_defaults()
    },

    methods: {
        search() {
            if (!this.valid) {
                this.error = "The form did not validate, please check the fields above"
                return
            }
            this.error = null
            this.showAdd = false
            this.currentQuery = {...this.query}
        },
        clear() {
            for (let key in this.query) {
                this.query[key] = null
            }
            this.error = null
            this.$refs.form.reset()
        },
        addNew() {
            this.showAdd = true
        },
        update_schema_add() {
            if (this.schema_add) {
                this.schema_add_ = JSON.parse(JSON.stringify(this.schema_add))
            } else (
                this.schema_add_ = null
            )
        },
        schema_add_set_defaults() {
            for (let key in this.schema_search.properties) {
                const prop = this.schema_search.properties[key]
                const value = this.query[key]
                if (prop["x-add-field"] && value) {
                    const addField = prop['x-add-field']
                    this.schema_add_.properties[addField]["default"] = value
                }
            }
        }
    },


}

</script>
<style lang="sass" scoped>
.add-new-form
    margin-top: 30px
</style>
