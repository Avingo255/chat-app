document.addEventListener('DOMContentLoaded', async function () {
    
    requestAnimationFrame(update_number_online_users);
    requestAnimationFrame(update_number_total_users);
});

async function update_number_online_users() {
    try {
        const response = await fetch(`${window.origin}/number-online-users`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                group_id: chat_group_id
            })
        });
        // no parameters to send in body

        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        } else {
            const data = await response.json();


            if (document.querySelector('.online-users').innerHTML !== "ONLINE: " + data) {
                document.querySelector('.online-users').innerHTML = "ONLINE: " + data;
            } 

        }

    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_number_online_users);
}

async function update_number_total_users() {
    try {
        const response = await fetch(`${window.origin}/number-total-users`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                group_id: chat_group_id
            })
        });
        // no parameters to send in body

        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        } else {
            const data = await response.json();

            if (document.querySelector('.total-users').innerHTML !== "MEMBERS: " + data) {
                document.querySelector('.total-users').innerHTML = "MEMBERS: " + data;
            } 

        }

    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_number_total_users);
}