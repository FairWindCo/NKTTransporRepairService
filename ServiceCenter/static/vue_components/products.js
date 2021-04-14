const fwproducts = {
    data() {
        return {
            view_category: true,
            count: 0,
            cars: [],
            category_loading: true,
            category_selected:null,
            category: null,
        }
    },
    methods: {
        onNodeSelect: function(leaf){
            console.log('LEAF', leaf)
           this.getProducts(leaf)
            console.log('LEAF', leaf)

        },
        getProducts: function (current_category = null){
            const current_level = current_category ? current_category.key : null
            get_data(this, '/ajax_category_product', {
                category_id: current_level
                //main: main
            }, data => {
                console.log(data.data_list);
                this.cars = data.data_list

            })
        },
        getCategory: function (current_category = null) {
            this.category_loading = true;
            const current_level = current_category ? current_category.key : ''
            if(current_category && current_category.leaf!==undefined && current_category.leaf){
                return
            }
            const main =  !current_category
            get_data(this, '/ajax_category', {
                level: current_level
                //main: main
            }, data => {
                console.log(data.data_list);
                this.category_loading = false;
                if(current_category){
                    current_category.children=data.data_list
                } else {
                    this.category = data.data_list
                }
            })
        },
    },
    mounted() {
        this.getCategory();
    },
    template: `
<div class="p-grid">
    <p-card class="p-col-12">
        <template #title>
            <div class="p-grid">
                <div class="col-12">Справочник товаров и категорий</div>
                <div :class="{
                    'col-3':view_category,
                    'fw-layout':true
                    }">
                <span v-if="view_category">Категории</span>                
                <a class="fw-layout-menu-button p-shadow-6 p-ripple" @click="view_category=!view_category">
                    <i :class="{
                    pi:true,
                    'pi-chevron-left': view_category,
                    'pi-chevron-right': !view_category,
                    }"></i>
                    <span class="p-ink" style="height: 35px; width: 35px; top: -3px; left: -4px;"></span>
                 </a></div>
                <div :class="{
                 'col-9': view_category,
                 'col-11': !view_category,
                 'fw-layout-right':true
                }">Товары</div>
            </div>
        </template>    
        <template #content>
                    <div class="p-grid">
                        <div class="col-3" v-if="view_category">
                            <p-tree :value="category" :loading="category_loading" selection-mode="single"
                             :selection-keys="category_selected"
                            @node-expand="getCategory" @node-select="onNodeSelect">
                                    <template #default="slotProps">
                                            {{slotProps.node.data}} <b>{{slotProps.node.label}}</b>
                                    </template>              
                            </p-tree>
                        </div>
                        <div :class="{'col-9': view_category,
                 'col-12': !view_category}">
                            <p-datatable :value="cars">
                                <p-column field="name" header="Name"></p-column>
                                <p-column field="code" header="1C Code"></p-column>
                                <p-column field="vendor_code" header="Vendor Code"></p-column>
                                <p-column field="brand_id" header="Brand"></p-column>
                            </p-datatable>
                        </div>
                    </div>           
        </template>
    </p-card>
</div>        
`
}