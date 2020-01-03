
import { mapGetters } from 'vuex'
import axios from 'axios'


function getCookie(name) {
  let value = "; " + window.document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


export default {

    state: {
        baseURL: null,
        csrf_token: null,
        connecting: false,
        connected: false,
        error: null,

        authenticated: false,
        roles: [],
    },

    mutations: {

        apiSetConnecting(state, baseURL) {
            state.baseURL = baseURL;
            state.connected = false;
            state.connecting = true;
            state.error = null;
        },

        apiSetError(state, message) {
            state.baseURL = null;
            state.connected = false;
            state.connecting = false;
            state.error = message;
        },

        apiSetConnected(state) {
            state.connected = true;
            state.connecting = false;
            state.error = null;
        },

        apiSetCSRFToken(state, csrf_token) {
            state.csrf_token = csrf_token
        },

        apiSetSessionInfo(state, sessionInfo) {
            state.authenticated = sessionInfo.authenticated;
            state.roles = sessionInfo.roles;
        },

    },

    actions: {

        connect(context, options) {
            context.commit('apiSetConnecting', options.baseURL)
            context.getters.api.get('@@session').then(response => {
                context.dispatch('setSessionInfo', {'sessionInfo': response.data.data})
                context.commit('apiSetConnected')
            }).catch(error => {
                context.commit('apiSetError', error)
            })
        },

        setSessionInfo(context, options) {
            context.commit('apiSetSessionInfo', options.sessionInfo)
            let csrf_token = getCookie('csrf_token');
            context.commit('apiSetCSRFToken', csrf_token)
        },

        refreshSessionInfo(context) {
            context.getters.api.get('@@session_info').then(response => {
                context.dispatch('setSessionInfo', {'sessionInfo': response.data.data})
            })
        },

    },

    getters: {
        apiAxiosOptions(state) {
            return {
                baseURL: state.baseURL,
                headers: {
                    'X-CSRF-Token': state.csrf_token,
                },
            }
        },
        api(state, getters) {
            if (state.baseURL) {
                return axios.create(getters.apiAxiosOptions)
            } else {
                return null
            }
        },
        csrf_token: s => s.csrf_token,
        authenticated: s => s.authenticated,
        roles: s => s.roles,
        apiError: s => s.error,
    },

}
