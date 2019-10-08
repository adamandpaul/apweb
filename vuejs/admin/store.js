
import axios from 'axios'

export default {

    state: {
        path: null,
        view: "main",
        loading: true,
        error: null,
        resource: null,
    },

    mutations: {
        loadingStart(state, path) {
            state.path = path
            state.loading = true
            state.error = null
            state.resource = null
        },
        loadingComplete(state, data) {
            state.loading = false
            state.error = null
            state.resource = data
        },
        loadingError(state, error) {
            state.loading = false
            state.error = error
            state.resource = null
        },
        setView(state, view) {
            state.view = view
        },
    },

    actions: {
        loadResource(context, opts) {
            context.commit('loadingStart', opts.path)
            context.getters.resourceApi.get("@@view-admin")
            .then((resp) => {
                context.commit("loadingComplete", resp.data.data)
            }).catch((error) => {
                context.commit("loadingError", error)
            })
        },
        changeResource(context, opts) {
            if (context.getters.path !== opts.path) {
                context.dispatch("loadResource", opts)
            }
        },
        changeView(context, opts) {
            context.commit('setView', opts.view)
        },
    },

    getters: {
        path: s => s.path,
        view: s => s.view,
        loading: s => s.loading,
        resource: s=> s.resource,

        error(state, getters, rootState, rootGetters) {
            return rootGetters.apiError || rootGetters.loginError || state.error
        },

        resourceApi(state, getters, rootState, rootGetters) {
            const options = {...rootGetters.apiAxiosOptions}
            options.baseURL = options.baseURL + getters.resourceURL
            return axios.create(options)
        },

        resourceURL(state) {
            if (state.path !== null) {
                const encodedParts = []
                for (let part of state.path) {
                    part = encodeURIComponent(part)
                    encodedParts.push(part)
                }
                return encodedParts.join('/')
            }
            return null
        },

    },

}
