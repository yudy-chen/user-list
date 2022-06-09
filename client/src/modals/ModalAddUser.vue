<template>
    <b-modal title="Add User" v-model="showModal"
        :hide-header-close=true :no-close-on-esc=true :no-close-on-backdrop=true
        size="md"
        id="modalAddUser"
    >

        <b-container>

            <div>Username</div>
            <div class="mb-2">
                <b-input autofocus v-model="userName"/>
            </div>

            <div>Age</div>
            <div class="mb-2">
                <b-input v-model="age"/>
            </div>

            <div>Photo</div>
            <div class="mb-2">
                <b-form-file
                    v-model="userPhoto"
                    :state="Boolean(userPhoto)"
                    placeholder="Choose a photo here..."
                    drop-placeholder="Drop file here..."
                    accept="image/*"
                    @change="attachImage"
                ></b-form-file>
            </div>

            <div class="container-img-user">
                <b-img class="img-user"
                    :src="userPhotoSrc"
                    @error="getDefaultImg"
                />
            </div>

        </b-container>

        <template v-slot:modal-footer="{}" >
            <div class="w-100">
                <b-btn variant="secondary" @click="cancelModal" :disabled="disableButton">
                    Cancel
                </b-btn>
                <b-btn variant="primary" class="float-right" @click="save" :disabled="disableButton">
                    Ok
                </b-btn>
            </div>
        </template>
        
        <b-overlay :show="showLoading" no-wrap />

    </b-modal>
</template>

<script>
    
    import axios  from 'axios'
    import { appConfig } from '../config';
    
    export default {
        name: 'ModalAddUser',
        props: {
            showModal: Boolean
        },
        data() {
            return{
                userPhoto: null,
                userPhotoSrc: "",
                userPhotoFile: null,
                userName: "",
                age: "",
                disableButton: false,
                showLoading: false,
                serverAddress: appConfig["SERVER_ADDRESS"],
                noPhotoImg: appConfig["SERVER_ADDRESS"] + "public/noPhoto.webp"
            }
        },
        methods: {
            getDefaultImg(e){
                e.target.src = this.noPhotoImg
            },
            cancelModal(){
                this.$emit("cancel")
            },
            save(){
                this.showLoading = true
                this.disableButton = true
                
                let that = this
                let formData = new FormData();
                
                formData.append('user_name', this.userName.trim());
                formData.append('age', parseInt(this.age.trim()));
                formData.append('userPhoto', this.userPhotoFile);
                
                axios.post(this.serverAddress + 'api/users/', formData)
                .then(response => {
                    that.showLoading = false
                    that.disableButton = false

                    if(response.data.status == "ok"){
                        that.$emit("success")
                    }else{
                        that.$emit("error", {
                            text  : response.data.msg,
                            title : "Error"
                        })
                    }
                })
                .catch(e => {
                    that.showLoading = false
                    that.disableButton = false
                    that.$emit("error", {
                        text  : "Server error",
                        title : "Alert"
                    })
                })

            },
            attachImage(e){
                const image = e.target.files[0];
                if(image != undefined){
                    const reader = new FileReader();
                    reader.readAsDataURL(image);
                    reader.onload = e =>{
                        this.userPhotoFile = image
                        this.userPhotoSrc = e.target.result;
                    };                
                }else{
                    this.userPhotoSrc = "";         
                    this.userPhotoFile = null;
                }
            },
            resetForm(){
                this.userPhoto = null
                this.userPhotoSrc = ""
                this.userPhotoFile = null
                this.userName = ""
                this.age = ""
            },
            evtModalShowing(bvEvent, modalId){
                if(modalId == "modalAddUser"){
                    this.resetForm()
                }
            }
        },
        mounted(){
            this.$root.$on('bv::modal::show', this.evtModalShowing)
        },
        beforeDestroy() {
            this.$root.$off('bv::modal::show', this.evtModalShowing);
        },        
    }

</script>

