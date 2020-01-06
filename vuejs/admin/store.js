
import axios from 'axios'

const DEFAULT_ROOT_NAVIGATION_NODE = {
    "title": "App",
    "path": [""],
    "named_resources": [],
}

function isPathsEqual(p1, p2) {
    if (p1 === null || p1 === null) {
        return p1 === p2
    }
    if (p1.length != p2.length)
        return false;
    for (var i = 0, l=p1.length; i < l; i++) {
        if (p1[i] != p2[i]) {
            return false
        }
    }       
    return true;
}

export default {

    state: {
        path: null,
        view: null,
        views: [],
        loading: true,
        error: null,
        title: null,
        description: null,
        thumbnail_url: null,
        has_workflow: false,
        workflow_actions: [],
        workflow_state: null,
        breadcrumbs: [DEFAULT_ROOT_NAVIGATION_NODE],
        rootNavigationNode: DEFAULT_ROOT_NAVIGATION_NODE,
    },

    mutations: {
        loadingStart(state, path) {
            state.path = path
            state.loading = true
            state.error = null

            // reset current workspace state
            state.description = null
            state.breadcrumbs = [state.rootNavigationNode]
            state.thumbnail_url = null
            state.has_workflow = false
            state.workflow_actions = []
            state.workflow_state = null
            state.views = []
        },
        reloadStart(state) {
            state.loading = true
            state.error = null
        },
        loadingComplete(state, data) {
            state.loading = false
            state.error = null

            // set workspace state
            state.title = data.title
            state.description = data.description
            state.thumbnail_url = data.thumbnail_url
            state.has_workflow = data.has_workflow
            state.workflow_actions = data.workflow_actions
            state.workflow_state = data.workflow_state
            state.breadcrumbs = data.breadcrumbs
            const views = []
            for (let v in data.views) {
                views.push({
                    "name": v,
                    ...data.views[v],
                })
            }
            views.sort((a, b) => (a.sort_key - b.sort_key))
            state.views = views
            if (views.length > 0 && state.view == null) {
                state.view = views[0].name
            }

            // Save root navigation node
            state.rootNavigationNode = state.breadcrumbs[0]
        },
        loadingError(state, error) {
            state.loading = false
            state.error = error
        },
        setView(state, view) {
            state.view = view 
        },
    },

    actions: {
        loadResource(context, opts) {
            context.commit('loadingStart', opts.path)
            context.getters.resourceApi.get("@@admin")
            .then((resp) => {
                context.commit("loadingComplete", resp.data.data)
            }).catch((error) => {
                context.commit("loadingError", error)
            })
        },
        reloadResource(context, opts) {
            context.commit('reloadStart')
            context.getters.resourceApi.get("@@admin")
            .then((resp) => {
                context.commit("loadingComplete", resp.data.data)
            }).catch((error) => {
                context.commit("loadingError", error)
            })
        },
        changeResourceOrView(context, opts) {
            if (!isPathsEqual(context.getters.path, opts.path)) {
                const view = opts.view || null
                context.commit("setView", view)
                context.dispatch("loadResource", opts)
            } else if  (opts.view && context.getters.selectedView != opts.view) {
                context.commit("setView", opts.view)
            }
        },
    },

    getters: {
        path: s => s.path,
        loading: s => s.loading,
        rootNavigationNode: s => s.rootNavigationNode,
        title: s => s.title,
        description: s => s.description,
        thumbnail_url: s => s.thumbnail_url,
        has_workflow: s => s.has_workflow,
        workflow_state: s => s.workflow_state,
        workflow_actions: s => s.workflow_actions,
        breadcrumbs: s => s.breadcrumbs,
        namedResources: s => s.breadcrumbs[s.breadcrumbs.length - 1].named_resources,
        links: s => s.breadcrumbs[s.breadcrumbs.length -1].links,
        viewsList: s => s.views,
        selectedView: s => s.view,
        viewsByName(state, getters) {
            const views = {}
            for (let v of getters.viewsList) {
                views[v.name] = v
            }
            return views
        },
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
                return encodedParts.join('/') || "/"
            }
            return null
        },

    },

}
