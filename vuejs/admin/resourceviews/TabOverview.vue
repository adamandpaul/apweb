<template>
    <div>

        <v-data-table
            :headers="summaryHeaders"
            :hide-default-header="true"
            :items="summary"
            :items-per-page="5"
          ></v-data-table>
        <ResourceMenu
            :items="namedResources" />
    </div>
</template>
<script>

import ResourceMenu from '../ResourceMenu.vue'
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

    components: {
        ResourceMenu,
    },

    computed: {
        ...mapGetters([
            'description',
            'namedResources',
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

</style>
