import { createStore } from 'vuex'

export default createStore({
  state: {
    token: sessionStorage.getItem('token'),
    role: sessionStorage.getItem('role'),
    id: sessionStorage.getItem('id'),
    email: sessionStorage.getItem('email'),
    sections: [],
    ebooks: [],
    associations: [],
    user_associations: [],
    users: [],
  },


  getters: {
    loggedIn(state) {
      return state.token != null
    },

    isAdmin(state) {
      return state.role === 'admin'
    },

    user(state) {
      return {
        token: state.token,
        id: state.id,
        role: state.role,
        email: state.email
      }
    },

    requested_associations(state) {
      return state.associations.filter(association => association.request_status === 'requested');
    },

    issued_associations(state) {
      return state.associations.filter(association => association.request_status === 'issued');
    },
  },


  mutations: {
    set_token(state, token) {
      state.token = token;
      sessionStorage.setItem('token', token);
    },

    set_role(state, role) {
      state.role = role;
      sessionStorage.setItem('role', role);
    },

    set_email(state, email) {
      state.email = email;
      sessionStorage.setItem('email', email);
    },

    set_id(state, id) {
      state.id = id;
      sessionStorage.setItem('id', id);
    },

    set_sections(state, sections) {
      state.sections = sections
    },

    set_ebooks(state, ebooks) {
      state.ebooks = ebooks
    },

    delete_section(state, section_id) {
      state.sections = state.sections.filter(section => section.id !== section_id);
      state.ebooks = state.ebooks.filter(ebook => ebook.section_id !== section_id);
    },

    delete_ebook(state, ebook_id) {
      state.ebooks = state.ebooks.filter(ebook => ebook.id !== ebook_id);
    },

    set_associations(state, associations) {
      state.associations = associations
    },

    set_user_associations(state, user_associations) {
      state.user_associations = user_associations
    },

    set_users(state, users) {
      state.users = users
    }
  },

  
  actions: {
    login({ commit }, user) {
      commit('set_token', user.token);
      commit('set_role', user.role);
      commit('set_id', user.id);
      commit('set_email', user.email);
    },

    logout({ commit }) {
      commit('set_token', null);
      commit('set_role', null);
      commit('set_id', null);
      commit('set_email', null);
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('role');
      sessionStorage.removeItem('id');
      sessionStorage.removeItem('email');
    },

    async getSections({ commit }) {
      try {
        const url = 'http://localhost:5000/api/sections';
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.state.token
          }
        });
        const data = await response.json();
        if (response.ok) {
          commit('set_sections', data);
        } else {
          console.log(data);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async getEbooks({ commit }) {
      try {
        const url = 'http://localhost:5000/api/ebooks';
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.state.token
          }
        });
        const data = await response.json();
        if (response.ok) {
          commit('set_ebooks', data);
        } else {
          console.log(data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async deleteSection({ commit }, section_id) {
      try {
        const url = 'http://localhost:5000/api/sections/' + section_id;
        const response = await fetch(url, {
          method: "DELETE",
          headers: {
            "Authentication-token": this.state.token
          }
        });
        if (response.ok) {
          console.log('Section deleted successfully');
          commit('delete_section', section_id);
        } else {
          const errorData = await response.json();
          alert(errorData.message);
        }
      } catch (error) {
        console.error('error while deleting section', error);
      }
    },

    async deleteEbook({ commit, dispatch }, ebook_id) {
      try {
        const url = 'http://localhost:5000/api/ebooks/' + ebook_id;
        const response = await fetch(url, {
          method: "DELETE",
          headers: {
            "Authentication-token": this.state.token
          }
        });
        if (response.ok) {
          console.log('Ebook deleted successfully');
          commit('delete_ebook', ebook_id);
          dispatch('getSections');
        } else {
          const errorData = await response.json();
          console.log(errorData.message);
        }
      } catch (error) {
        console.error('error while deleting ebook', error);
      }
    },

    async getAssociations({ commit }) {
      try {
        const url = 'http://localhost:5000/api/associations';
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.state.token
          }
        });
        const data = await response.json();
        if (response.ok) {
          commit('set_associations', data);
        } else {
          console.log(data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async getUserAssociations({ commit }) {
      try {
        const url = 'http://localhost:5000/api/associations/' + this.state.id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.state.token
          }
        });
        const data = await response.json();
        if (response.ok) {
          commit('set_user_associations', data);
        } else {
          console.log(data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async getUsers({ commit }) {
      try {
        const url = 'http://localhost:5000/api/users';
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.state.token
          }
        });
        const data = await response.json();
        if (response.ok) {
          commit('set_users', data);
        } else {
          console.log(data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
  })
