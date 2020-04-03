<template>
    <v-card flat>
        <v-card-title>{{ title_ }}</v-card-title>

        <v-card-text v-if="loading" class="text-center">
            <v-progress-circular indeterminate />
        </v-card-text>

        <v-card-text v-if="loadingError">
            <request-error :error="loadingError" />
        </v-card-text>

        <v-card-text>
            <v-jsonschema-form ref="form" v-if="schema_search" :schema="schema_search" :model="searchQuery" :options="searchOptions"/>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="clear">Clear</v-btn>
            <v-btn color="primary" @click="search">Search</v-btn>
            <v-btn class="btn-add-new" v-if="schema_add" color="secondary" @click="addNew">Add New Item</v-btn>
        </v-card-actions>

        <v-card-text v-if="!showAdd">
            <collection-search-results :query="searchCurrentQuery" :resourceURL="resourceURL" :tileNewTab="tileNewTab">
                <template v-slot:tile-start="{resource}"><slot name="tile-start" :resource="resource"></slot></template>
                <template v-slot:tile-left="{resource}"><slot name="tile-left" :resource="resource"></slot></template>
                <template v-slot:tile-end="{resource}"><slot name="tile-end" :resource="resource"></slot></template>
            </collection-search-results>
        </v-card-text>

        <v-card-text v-if="showAdd">
            <collection-add :schema="schema_add_" :resourceURL="resourceURL">
                <template v-slot:tile-start="{resource}"><slot name="tile-start" :resource="resource"></slot></template>
                <template v-slot:tile-left="{resource}"><slot name="tile-left" :resource="resource"></slot></template>
                <template v-slot:tile-end="{resource}"><slot name="tile-end" :resource="resource"></slot></template>
            </collection-add>
        </v-card-text>

    </v-card>
</template>
<script>


export default {


    props: {
        resourceURL: {type: String, default: null},
        title: {type: String, default: null},
        tileNewTab: {},
    },

    data() {
        return {
            loading: true,
            loadingError: null,
            options: {},
            searchOptions: {
                debug: false,
                disableAll: false,
                autoFoldObjects: false,
            },
            searchError: null,
            searchQuery: {},
            searchCurrentQuery: null,
            showAdd: false,
            schema_add_: null,
        }
    },

    computed: {

        resourceApi() {
            return this.$store.getters.resourceApiForResourceURL(this.resourceURL)
        },

        title_() {
            return this.title || this.options.title || "Browse..."
        },


        schema_search() {
            return this.options["schema_search"]
        },
        schema_add() {
            return this.options["schema_add"]
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
        searchQuery: {
            handler() {
                this.schema_add_set_defaults()
            },
            deep: true,
        },
    },

    async mounted() {
        await this.load()
        this.update_schema_add()
        this.schema_add_set_defaults()
    },

    methods: {
        async load() {
            this.loading = true
            this.loadingError = null
            let resp = null
            try {
                resp = await this.resourceApi.get('@@admin-browse')
            } catch (err) {
                this.loadingError = err
                this.loading = false
                return
            }
            this.options = resp.data.data
            this.loading = false
        },

        search() {
            this.searchError = null
            this.showAdd = false
            this.searchCurrentQuery = {...this.searchQuery}
        },
        clear() {
            for (let key in this.query) {
                this.query[key] = null
            }
            this.error = null
            this.searchCurrentQuery = null
            this.showAdd = false
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
                const value = this.searchQuery[key]
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
