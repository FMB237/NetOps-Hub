// device Creation gestion 
const btn  = document.getElementById('testConnection');
btn.addEventListener('click',async()=>{

 const ip =document.querySelector('[name =ip_address]').value;
 const port = document.querySelector("[name= ssh_port]").value;
 const result = document.getElementById('connectionResult');



 result.innerHTML =
        "<div class='alert alert-info'>Testing...</div>";

    const response = await fetch(
        "/api/network/test",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                ip_address: ip,
                port: Number(port),
            }),
        }
    );

    const data = await response.json();

    if (data.reachable) {

        result.innerHTML = `
            <div class="alert alert-success">

                ✅ ${data.message}<br>

                Latency: ${data.latency}

            </div>
        `;

    } else {

        result.innerHTML = `
            <div class="alert alert-danger">

                ❌ ${data.message}

            </div>
        `;
    }

});
