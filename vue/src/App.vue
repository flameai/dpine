<template>
  <b-container class="bv-example-row">      
    <b-row class="mt-5">
      <b-col>
        <h4>Создать редирект</h4>
        <b-form inline>
          <label class="sr-only" for="inline-form-input-url">Адрес URL</label>
          <b-form-input
            id="inline-form-input-url"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="Введите ссылку сюда"
            v-model="destUrl"
          ></b-form-input>

          <label class="sr-only" for="inline-form-input-slug">Субпарт</label>
          <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
            <b-form-input id="inline-form-input-slug" placeholder="Введите сюда короткий адрес или получите автоматический"
            v-model="subpart"
            ></b-form-input>
          </b-input-group>
          <b-button variant="primary" class="mt-3" @click="createRedirect">Создать</b-button>
        </b-form>        
      </b-col>
      <b-col></b-col>      
    </b-row>

    <b-row class="mt-5">
      <b-col>
        <b-table v-if="redirects.length" striped hover :items="redirects"></b-table>
        <div v-else><h5> Вы еще не создали ни одного редиректа</h5></div>
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
      next: null,
      previous: null,
      count: 0,
      destUrl: null,
      subpart: null
    }
  },
  mounted: function () {
    this.load()
  },
  methods:{
    load: function(){
      this.$axios.get(`${this.rootURL}/url/`, {  
  withCredentials: true
}).then(data => {
      this.redirects = data.data.results
      this.count = data.data.count
      this.next = data.data.next
      this.previous = data.data.previous
    })      
    },
    createRedirect(){
      let data = {'dest_url': this.destUrl, 'subpart': this.subpart}
      this.axios.post(`${this.rootURL}/url/`, data).then(data =>
      console.log(data)      
      )
      this.load()
    }
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
