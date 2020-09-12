<template>
    <div>
    <v-file-input
      v-model="images"
      color="deep-purple accent-4"
      counter
      accept="iamge/png, image/jpeg, image/bmp"
      label="Image Input"
      multiple
      placeholder="Select your images"
      prepend-icon="mdi-camera"
      outlined
      :show-size="1000"
    >
      <template v-slot:selection="{ index, text }">
        <!--中にちっちゃく表示される楕円のやつ-->
        <v-chip 
          color="deep-purple accent-4"
          dark
          label
          small
        >
          {{ text }}
        </v-chip>
      </template>
    </v-file-input>
    <v-btn
        color="blue-grey"
        class="ma-2 white--text"
        @click="upload()"
      >
        Upload
        <v-icon right dark>mdi-cloud-upload</v-icon>
      </v-btn>
    <span id="upload-test">testttt</span>
    <v-img :src="picture"></v-img>
    
    <v-sheet
        class="mx-auto"
        elevation="8"
        max-width="800"
      >
        <v-slide-group
          class="pa-4"
          center-active
        >
          <v-slide-item
            v-for="(item,index) in picture"
            :key="index"
            v-slot:default="{ active, toggle }"
          >
            <v-card
              class="ma-4"
              height="200"
              width="100"
              @click="toggle"
            >
              <v-row
                class="fill-height"
                align="center"
                justify="center"
              >
                 <v-img
                  height="200"
                  width="200"
                  :src="item">
                  </v-img>
              </v-row>
            </v-card>
          </v-slide-item>
        </v-slide-group>
      </v-sheet>
    </div>
</template>

<script>
    export default {
        name: 'Upload',
        components: {
        },
        data(){
            return{
                images :[],
                picture : []
            }
        },
        methods:{
            async upload(){
                const files = this.images
                for(let i = 0,numFiles = files.length;i < numFiles;i++){
                    let file = files[i]
                    if(this.checkFile(file)){
                        this.picture.push(await this.getBase64(file))
                    }
                }
            },
            getBase64(file){
                return new Promise((resolve,reject) => {
                    const reader = new FileReader()
                    reader.readAsDataURL(file)
                    reader.onload = () => resolve(reader.result)
                    reader.onerror = error => reject(error)
                })
            },
            checkFile(file){
                let result = true
                const SIZE_LIMIT = 10000000 // 10MB
                if(!file){
                    result = false
                }
                if(file.size > SIZE_LIMIT){
                    result = false
                }
                return result
            }
        },

    }

</script>
<style>
</style>
