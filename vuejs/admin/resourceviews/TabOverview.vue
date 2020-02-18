<template>
    <div>
        <v-data-table
            class="data-table"
            :headers="summaryHeaders"
            :hide-default-header="true"
            :items="summary"
            :items-per-page="10"
          ></v-data-table>
    </div>
</template>
<script>

import {mapGetters} from 'vuex'

export default {

    props: {
        data: Object,
    },

    data() {
        return {
            summaryHeaders: [
                {
                    text: "Summary Information",
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
        ...mapGetters([
            'description',
        ]),
        summary() {
            return this.data.summary
        },
    },

}
</script>
<style lang="sass" scoped>

.description
    font-weight: bold

.data-table
    margin-top: 32px

</style>
