<template>
    <div>
        <v-form ref="form" v-model="valid" @submit.prevent="add" :update-key="updateKey">
            <v-card flat>
                <v-card-title>{{ this.schema.title }}</v-card-title>
                <v-card-text>
                    <v-jsonschema-form v-if="schema" :schema="schema" :model="value" :options="formOptions" @error="showError" />
                    <v-alert v-if="error" type="error" text>
                        {{ error }}
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="clear">Clear Form</v-btn>
                    <v-btn :loading="inProgress" color="primary" @click="add">Add</v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
        <request-error v-if="requestError" :error="requestError" />
        <p v-if="itemsAdded.length > 0">
           Added {{ itemsAdded.length }} item(s)
        </p>
        <div v-for="(item, idx) in itemsAdded" :key="idx">
            <component :is="item.ui || 'resource-tile'" :tile="item" />
        </div>
    </div>
</template>
<script>

import ResourceMenu from '../ResourceMenu.vue'
import {mapGetters} from 'vuex'

export default {

    props: {
        data: [Object, null],
        options: [Object, null],
    },

    data() {
        return {
            value: {},
            updateKey: 0,
            valid: false,
            error: null,
            requestError: null,
            formOptions: {
                debug: false,
                disableAll: false,
                autoFoldObjects: false,
            },
            inProgress: false,
            itemsAdded: [],
        }
    },
    computed: {
        ...mapGetters([
            'resourceApi',
        ]),
        schema() {
            return this.data || this.options.schema
        }
    },

    methods: {
        showError(err) {
            this.error = err
        },
        add() {
            if (!this.valid) {
                this.showError("The form did not validate, please check the fields above")
                return
            }
            this.inProgress = true
            this.requestError = null
            this.resourceApi.post('', this.value)
                .then(this.handleResponse)
                .catch(this.handleError)
        },
        clear() {
            for (let key in this.value) {
                this.value[key] = null
            }
            this.error = null
            this.$refs.form.reset()
        },
        handleResponse(resp) {
            this.itemsAdded.unshift(resp.data.data)
            this.inProgress = false
            this.clear()
        },
        handleError(err) {
            this.inProgress = false
            this.requestError = err
        },
    }

}
</script>
