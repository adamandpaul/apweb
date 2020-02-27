<template>
    <v-card outlined>
        <v-data-table
            class="data-table"
            :headers="tableHeaders"
            :hide-default-header="true"
            :hide-default-footer="hideFooter"
            :items="properties"
            :items-per-page="itemsPerPage"
        ></v-data-table>
    </v-card>
</template>
<script>

import {mapGetters} from 'vuex'

export default {

    props: {
        data: Object,
    },

    data() {
        return {
            tableHeaders: [
                {
                    text: "Key",
                    align: "left",
                    sortable: false,
                    value: "title",
                },
                {
                    text: "Value",
                    align: "left",
                    sortable: false,
                    value: "value",
                },
            ],
        }
    },

    computed: {
        properties() {
            return this.data.properties
        },
        itemsPerPage() {
            return 10
        },
        hideFooter() {
            return this.properties.length <= this.itemsPerPage
        },
    },

}
</script>
<style lang="sass" scoped>
</style>
