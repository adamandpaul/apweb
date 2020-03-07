<template>
    <div>      
        <v-input>
            <resource-tile class="resource-tile" :resourceURL="resourceURL" :newTab="true">
                <template v-slot:start>
                    <v-card-text>{{ label }}</v-card-text>
                </template>
                <template v-slot:left>
                    <v-list-item-action class="left-action">
                        <v-btn class="grey lighten-2" text @click="clear"><v-icon>close</v-icon></v-btn>
                    </v-list-item-action>
                </template>
                <template v-slot:no-resource>
                    <v-btn class="grey lighten-2" text @click="browse">Browse...</v-btn>
                </template>
            </resource-tile>
        </v-input>

        <v-dialog @click:outside="cancelBrowse" :value="browseDialog" max-width="980">

            <v-card>
                <v-toolbar dark color="secondary">
                    <v-toolbar-title>{{ label }}: Browse</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn text fab @click="cancelBrowse"><v-icon>close</v-icon></v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <v-card-text>
                    <collection-browse :resourceURL="collectionURL" :tileNewTab="true">
                        <template v-slot:tile-left="{resource}">
                            <v-list-item-action class="left-action">
                                <v-btn
                                  text
                                  class="open primary right-action-btn"
                                  @click="input(resource)">
                                    <v-icon>mdi-arrow-right</v-icon>
                                </v-btn>
                            </v-list-item-action> 
                        </template>
                    </collection-browse>
                </v-card-text>

            </v-card>

        </v-dialog>


    </div>
</template>
<script>
export default {
    props: ["label", "value", "collectionURL"],

    data() {
        return {
            browseDialog: false,
        }
    },

    computed: {
        resourceURL() {
            if (this.value) {
                return this.collectionURL + "/" + this.value
            } else {
                return null
            }
        },
    },

    methods: {
        input(resource) {
            this.browseDialog = false
            let value = resource.name
            this.$emit("input", value)
        },
        browse(e) {
            this.browseDialog = true
        },
        cancelBrowse() {
            this.browseDialog = false
        },
        clear() {
            this.$emit("input", null)
        },
    },

}
</script>
<style lang="sass" scoped>
.resource-tile
    width: 100%
</style>