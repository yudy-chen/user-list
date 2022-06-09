<template>
    <b-container class="mt-3 pt-1 pb-3">
        
        <b-row cols-md="2" cols-lg="2" cols-xl="2" class="container-row-user-list">
            <b-col>
                <b-list-group class="list-group-user">
                    <div>
                        <div class="container-list-user-title" v-if="userData.length == 0">
                            <span>No user</span>
                        </div>
                        <div class="container-list-user-title" v-else>
                            <span>List User</span>
                        </div>
                        <b-list-group-item v-if="userData.length > 0" class="list-group-item-user" v-for="(user, idx) in userData" :key="`card-user-${idx}`">
                            <b-card>
                                <div class="p-2 container-header-user">
                                    <div class="header-user-name">
                                        <span>
                                            {{user.userName}}
                                        </span>
                                        <span v-if="user.age > 1">
                                            ({{user.age}} years old)
                                        </span>
                                        <span v-else>
                                            ({{user.age}} year old)
                                        </span>
                                    </div>
                                    <div class="button-remove-user">
                                        <b-btn variant="danger" size="sm" class="float-right" @click="confirmDeleteUser(user.id, user.userName)">
                                            <i class="fa fa-trash"></i>
                                        </b-btn>
                                    </div>
                                </div>
                                <div class="p-3 container-img-user">
                                    <b-img class="img-user" 
                                        :src="user.photoPath"
                                        @error="getDefaultImg"
                                    />
                                </div>
                            </b-card>
                        </b-list-group-item>
                    </div>
                </b-list-group>

                <div class="mt-2">
                    <b-btn variant="success" size="sm" @click="exportToCSV">
                        <i class="fa fa-save"></i>
                        <span class="p-2">Export CSV</span>
                    </b-btn>
                    <b-btn variant="primary" class="float-right" size="sm"  @click="createNewUser">
                        <i class="fa fa-plus-circle"></i>
                        <span class="p-2">Add</span>
                    </b-btn>
                </div>
            </b-col>
        </b-row>

        <ModalInfo
            :showModal="showModalInfo"
            :bodyText="infoText"
            :titleText="infoTitle"
            @close="showModalInfo=false"
        />
        
        <ModalAddUser
            :showModal="showModalAddUser"
            @cancel="showModalAddUser=false"
            @success="addUserSuccesss"
            @error="addUserError"
        />

        <ModalConfirm
            :showModal="showModalConfirm"
            :confirmedTopic="confirmedTopic"
            :bodyText="confirmText"
            :titleText="confirmTitle"
            @cancel="showModalConfirm=false"
            @ok="okConfirm"
        />

        <b-overlay :show="showLoading" no-wrap />

    </b-container>
</template>

<script>
    
    import axios  from 'axios'
    
    import '../css/MainLayout.css'
    import '../css/App.css'
    
    import ModalInfo from  '../modals/ModalInfo'
    import ModalAddUser from  '../modals/ModalAddUser'
    import ModalConfirm from  '../modals/ModalConfirm'
    import { appConfig } from '../config';
    
    export default {
        name: 'MainLayout',
        components: { ModalInfo, ModalAddUser, ModalConfirm },
        data() {
            return{
                infoText: "",
                infoTitle: "",
                
                confirmedTopic: "",
                confirmText: "",
                confirmTitle: "",
                
                showModalConfirm: false,
                showModalInfo: false,
                showModalAddUser: false,
                showLoading: false,
                
                userData: [],
                userTobDeleted: null,
                serverAddress: appConfig["SERVER_ADDRESS"],
                noPhotoImg: appConfig["SERVER_ADDRESS"] + "public/noPhoto.webp"
            }
        },
        methods: {
            confirmDeleteUser(userID, userName){
                this.confirmText = "Do you want to delete user " + userName + "?"
                this.confirmTitle = "Confirm delete"
                this.userTobDeleted = userID
                this.confirmedTopic = "deleteUser"
                this.showModalConfirm = true
            },
            createNewUser(){
                this.showModalAddUser = true
            },
            getDefaultImg(e){
                e.target.src = this.noPhotoImg
            },
            getAllUsers(){
                let that = this
                that.userData = []
                that.showLoading = true

                axios.get(this.serverAddress + 'api/users/')
                .then(response => {
                    that.showLoading = false
                    that.userData = response.data
                })
                .catch(e => {
                    that.showLoading = false
                    that.infoText = "Server error"
                    that.showModalInfo = true
                    that.infoTitle = "Alert"
                })
            
            },
            addUserSuccesss(){
                this.showLoading = false
                this.showModalAddUser = false
                this.infoText = "Add user success"
                this.showModalInfo = true
                this.infoTitle = "Info"
                this.getAllUsers()
            },
            addUserError(info){
                this.showLoading = false
                this.infoText = info.text
                this.infoTitle = info.title
                this.showModalInfo = true
            },
            deleteUser(){
                this.showLoading = true
                
                let that = this
                
                axios.delete(this.serverAddress + 'api/users/'+ this.userTobDeleted + '/')
                .then(response => {
                    that.showLoading = false
                    if(response.data.status == "ok"){
                        that.infoText = "Remove user success"
                        that.showModalInfo = true
                        that.infoTitle = "Info"
                        that.getAllUsers()
                    }else{
                        that.infoText = response.data.msg
                        that.showModalInfo = true
                        that.infoTitle = "Error"
                    }
                })
                .catch(e => {
                    that.showLoading = false
                    that.infoText = "Server error"
                    that.showModalInfo = true
                    that.infoTitle = "Alert"
                })
            
            },
            okConfirm(topic){
                this.showModalConfirm = false
                if(topic == "deleteUser"){
                    this.deleteUser()
                }
            },
            exportToCSV(){
                window.open(this.serverAddress + 'users/export', "_blank")
            }
        },
        mounted(){
            this.getAllUsers()
        }
    }

</script>