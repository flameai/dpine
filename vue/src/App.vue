<template>
  <b-container class="bv-example-row">      
    <b-row>
      <b-col>
        <b-form inline>
          <label class="sr-only" for="inline-form-input-url">Адрес URL</label>
          <b-form-input
            id="inline-form-input-url"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="Введите ссылку сюда"
          ></b-form-input>

          <label class="sr-only" for="inline-form-input-slug">Субпарт</label>
          <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
            <b-form-input id="inline-form-input-slug" placeholder="Введите сюда короткий адрес"></b-form-input>
          </b-input-group>
          <b-button variant="primary" mt-2 >Создать</b-button>
        </b-form>        
      </b-col>
      <b-col></b-col>      
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
    }
  },
  mounted: function () {
    return console.log(this.axios.get(`${this.rootURL}/url/`))    
  },
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
