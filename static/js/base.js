let storyBtn = document.querySelector("#storyBtn");
        let jobBtn = document.querySelector("#jobBtn");
        let submitBtn = document.querySelector("#filterSubmit");
        let formInput = document.querySelector("#formInput");
        let last_id = null;
        let latest_id = 0;
        let new_alert = document.querySelector('#new-info-alert');

        storyBtn.addEventListener('click', ()=>{
          formInput.value = "story";
          submitBtn.click();
        });

        jobBtn.addEventListener('click', ()=>{
          formInput.value = "job";
          submitBtn.click();
        });

        const get_id = async ()=>{
          try {
            const data = await fetch(`${window.location.origin}/api/v1/stories/latest/`, {
              method: 'GET'
            });
            let res = await data.json()
            let latest_id = res.id;
            
            console.log(last_id);
            if (!last_id) {
              // do nothing
            }
            else if (last_id !== latest_id){
              new_alert.classList.remove('d-none');
            }
            else new_alert.classList.add('d-none');
            last_id = latest_id;
          } catch (error) {
            console.log(error)
          }
        }

        let timer = setInterval(get_id, 1000*60*5);