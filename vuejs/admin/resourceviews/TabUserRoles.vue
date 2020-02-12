<template>
    <div>
        <v-toolbar dense flat>
            <v-spacer />
            <v-toolbar-items>
                <v-text-field label="Filter" v-model="filter" />
            </v-toolbar-items>
        </v-toolbar>
        <v-list>
            <v-list-item :input-value="role.selected" color="green" v-for="role in filteredSortedRoles" :key="role.role_name" @click="toggle(role.role_name)">
                <v-list-item-content>
                    {{ role.role_name }}
                    <request-error v-if="role.error" :error="role.error" />
                </v-list-item-content>
                <v-list-item-action>
                    <v-btn :loading="role.inProgress" icon @click="toggle(role.role_name)">
                        <v-icon v-if="role.selected">{{ mdiCheckCircleOutline }}</v-icon>
                        <v-icon v-if="!role.selected">{{ mdiCheckboxBlankCircleOutline }}</v-icon>
                    </v-btn>
                </v-list-item-action>
            </v-list-item>
        </v-list>
        <v-card class="mt-5" outlined>
            <v-card-title>New Role</v-card-title>
            <v-card-text>
                <v-text-field label="Role" v-model="newRole" />
            </v-card-text>
            <v-card-actions>
                <v-spacer />
                <v-btn color="primary" :disabled="newRole.length == 0" @click="assignNewRole">Add</v-btn>
            </v-card-actions>
        </v-card>

    </div>
</template>

<script>

import objectHash from 'object-hash'
import {mapGetters} from 'vuex'
import {mdiCheckboxBlankCircleOutline} from '@mdi/js'
import {mdiCheckCircleOutline} from '@mdi/js'

export default {

    props: {
        data: [Object, null],
        options: [Object, null],
    },

    data() {
        return {
            mdiCheckboxBlankCircleOutline,
            mdiCheckCircleOutline,
            roles: {},
            newRole: "",
            sortedRoles: [],
            filter: "",
        }
    },

    computed: {

        ...mapGetters([
            "resourceApi",
        ]),

        filteredSortedRoles() {
            const roles = []
            const filter = this.filter.toLowerCase()
            for (let role of this.sortedRoles) {
                const role_name = role.role_name.toLowerCase()
                if (role_name.indexOf(filter) >= 0) {
                    roles.push(role)
                }
            }
            return roles
        }

    },

    methods: {

        refreshSortedRoles() {
            const roles = []
            for (var role_name in this.roles) {
                const role = this.roles[role_name]
                roles.push(role)
            }
            roles.sort(function(a, b){
                var keyA = a.sortKey,
                    keyB = b.sortKey;
                // Compare the 2 dates
                if(keyA < keyB) return -1;
                if(keyA > keyB) return 1;
                return 0;
            })
            this.sortedRoles = roles
        },

        toggle(role_name) {
            const role = this.roles[role_name]
            if (role.selected) {
                this.revoke(role.role_name)
            } else {
                this.assign(role.role_name);
            }
        },

        assignNewRole() {
            this.assign(this.newRole)
            this.newRole = ""
            this.filter = ""
        },

        assign(role_name) {
            role_name = role_name.trim()
            let roleInfo = this.roles[role_name]
            if (!roleInfo) {
                this.roles[role_name] = roleInfo = {
                    role_name: role_name,
                    selected: false,
                    inProgress: false,
                    error: false,
                    sortKey: this.roles.length,
                }
                this.refreshSortedRoles()
            }
            roleInfo.inProgress = true
            this.resourceApi.post(
                "@@admin-assign-role",
                {"role": role_name},
                {"role_name": role_name},
            ).then(this.assignHandleSuccess).catch(this.handleError)
        },

        revoke(role_name) {
            role_name = role_name.trim()
            let roleInfo = this.roles[role_name]
            roleInfo.inProgress = true
            this.resourceApi.post(
                "@@admin-revoke-role",
                {"role": role_name},
                {"role_name": role_name},
            ).then(this.revokeHandleSuccess).catch(this.handleError)
        },

        assignHandleSuccess(resp) {
            const role_name = resp.config.role_name
            this.roles[role_name].inProgress = false
            this.roles[role_name].selected = true
        },

        revokeHandleSuccess(resp) {
            const role_name = resp.config.role_name
            this.roles[role_name].inProgress = false
            this.roles[role_name].selected = false
        },
        handleError(err) {
            const role_name = err.config.role_name
            this.roles[role_name].inProgress = false
            this.roles[role_name].error = err
        },
    },

    mounted() {

        // compile the this.roles dictionary
        const current_roles = this.data.current_roles
        const roles = {}
        const selectedRoles = []
        for (let role_name of this.data.assigned_roles) {
            selectedRoles.push(role_name)
        }

        for (let i = 0; i < current_roles.length; i++) {
            const role_name = current_roles[i]
            roles[role_name] = {
                role_name: role_name,
                selected: selectedRoles.indexOf(role_name) >= 0,
                inProgress: false,
                error: false,
                sortKey: i,
            }
        }
        this.roles = roles
        this.refreshSortedRoles()
    },




}
</script>