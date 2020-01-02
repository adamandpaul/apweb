<template>
    <div class="resource-header">
        <div class="container">
            <div v-if="thumbnail_url" class="thumbnail">
                <img :src="thumbnail_url" />
            </div>
            <div class="details">
                <div class="title">{{ title }}</div>
                <div class="description">{{ description }}</div>
            </div>
            <div v-if="has_workflow" class="workflow">
                <BtnWorkflow :loading="workflowActionInProgress" :state="workflow_state" :actions="workflow_actions" @menuclick="workflowAction" />
            </div>
        </div>
        <div v-if="workflowError" class="container">
            <request-error :error="workflowError" />
        </div>
    </div>
</template>
<script>

import BtnWorkflow from './BtnWorkflow.vue'
import {mapGetters} from 'vuex'

export default {

    data() {
        return {
            "workflowActionInProgress": false,
            "workflowError": null,
        }
    },

    components: {
        BtnWorkflow,
    },

    computed: {
        ...mapGetters([
            'title',
            'description',
            'thumbnail_url',
            'has_workflow',
            'workflow_state',
            'workflow_actions',
            'resourceApi',
        ]),
    },

    methods: {
        workflowAction(action) {
            this.workflowError = null
            this.workflowActionInProgress = true
            this.resourceApi.post("@@admin-workflow-action", {"action": action})
                .then(this.workflowActionResponse)
                .catch(this.workflowActionError)
        },
        workflowActionResponse(resp) {
            this.workflowActionInProgress = false
            this.$root.$emit("resourceUpdated")
        },
        workflowActionError(err) {
            this.workflowActionInProgress = false
            this.workflowError = err
        },
    },

}


</script>
<style lang="sass" scoped>

.resource-header
    background: #f5f5f5

    .container
        padding: 56px 0 32px 0
        display: flex
        align-items: center
        margin: 0 auto
        max-width: 980px

    >*
        flex-grow: 0

    .details
        flex-grow: 1

    .thumbnail
        background: white
        padding: 8px
        border-radius: 5px
        margin-right: 24px
        box-shadow: 3px 3px 6px 0px rgba(0,0,0,0.08)

        img
            display: block
            width: 128px

</style>
