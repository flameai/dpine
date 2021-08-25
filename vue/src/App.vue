<template>
  <b-container class="bv-example-row">      
    <b-row class="mt-5">
      <b-col>
        <h4>Создать редирект</h4>
        <b-form inline>
          <label class="sr-only" for="inline-form-input-url">Адрес URL</label>
          <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
            <b-form-input
              id="inline-form-input-url"
              class="mb-2 mr-sm-2 mb-sm-0"
              placeholder="Введите ссылку сюда"
              v-model="destUrl"
              :state="!destUrlError"
            ></b-form-input>
            <b-form-invalid-feedback :state="!destUrlError">
                {{ destUrlErrorText }}
            </b-form-invalid-feedback>
          </b-input-group>

          <label class="sr-only" for="inline-form-input-slug">Субпарт</label>
          <b-input-group class="mb-2 mr-sm-2 mb-sm-0" >
            <b-form-input id="inline-form-input-subpart" placeholder="Введите сюда короткий адрес или получите его автоматически"
            v-model="subpart"
            :state="!subpartError"
            ></b-form-input>
            <b-form-invalid-feedback  v-if="subpartError" :state="!subpartError">
                {{ subpartErrorText }}
            </b-form-invalid-feedback>
          </b-input-group>
          <b-button variant="primary" class="mt-3" @click="createRedirect">Создать</b-button>
        </b-form>        
      </b-col>
      <b-col></b-col>      
    </b-row>

    <b-row class="mt-5">
      <b-col>
        <template v-if="redirects.length">
          <b-table
            striped 
            hover 
            :items="redirects" 
            id="redirects"            
            :per-page="perPage"
            :current-page="currentPage"
            :fields="[{ key: 'dt', label: 'Дата и время', formatter: (value) => {
                        let date = new Date(value)
                        return date.toLocaleString()
                      }}, 
                      { key: 'dest_url', label:'Адрес ссылки' }, 
                      { key: 'subpart', label:'Короткий адрес' }]"
            >
          </b-table>

          <b-pagination
            v-model="currentPage"
            :total-rows="redirects.length"
            :per-page="perPage"
            aria-controls="redirects"
          ></b-pagination>
        </template>
        <template v-else>
          <div><h5> Вы пока еще не создали ни одного редиректа</h5></div>
        </template>
      </b-col>
    </b-row>


  </b-container>    
</template>

<script>

export default {
  name: 'App',
  components: {    
  },  
  data: () => {
    return {
      rootURL: "http://127.0.0.1:8009",
      redirects: [],
      currentPage: 1,      
      perPage: 10,
      destUrl: null,
      subpart: null,
      validationErrors: null
    }
  },
  mounted: function () {
    this.load()
  },
  methods:{    
    load: function(){
      this.$axios.get(`${this.rootURL}/url/`, {
      withCredentials: true,
      headers: {
      }
    }).then(data => {
      this.redirects = data.data      
    })      
    },
    createRedirect(){
      let data = {'dest_url': this.destUrl, 'subpart': this.subpart}
      this.$axios.post(`${this.rootURL}/url/`, 
      data, {
      withCredentials: true
      }).then(data => {
        console.log(data)
        this.load()
        this.validationErrors = null
        }
      ).catch(error => this.validationErrors = error.response.data)
      
    }
  },
  computed: {
    destUrlError(){
      return this.validationErrors ? 'dest_url' in this.validationErrors: false
    },
    subpartError(){
      return this.validationErrors ? 'subpart' in this.validationErrors: false
    },
    destUrlErrorText(){
      return this.destUrlError ? this.validationErrors.dest_url.join(' ') : ''
    },
    subpartErrorText(){
      return this.subpartError ? this.validationErrors.subpart.join(' '): ''
    },
  }  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
