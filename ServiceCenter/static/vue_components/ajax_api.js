function get_data(vue, url, params = {}, processor = null) {
    axios.get(url, {
        params: params
    })
        .then(function (response) {
            if(processor && processor instanceof Function){
                processor(response.data)
            }
        })
        .catch(function (error) {
            let answer = 'Error! Could not reach the API. ' + error
            vue.$toast.add({severity: 'error', summary: 'Error Message', detail: answer, life: 3000});
        })
}
function post_data(vue, url, params = {}, processor = null) {
    axios.post(url, {
        params: params
    })
        .then(function (response) {
            if(processor && processor instanceof Function){
                processor(response.data)
            }
        })
        .catch(function (error) {
            let answer = 'Error! Could not reach the API. ' + error
            vue.$toast.add({severity: 'error', summary: 'Error Message', detail: answer, life: 3000});
        })
}