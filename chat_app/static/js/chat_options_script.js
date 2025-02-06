// chat_group_id is a global variable that is set externally in js/get_group_id.js

document.addEventListener('DOMContentLoaded', async function () {
    requestAnimationFrame(update_group_user_list);
});

async function update_group_user_list() {
    try {
        const response = await fetch(`${window.origin}/group-user-details`, {
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

            let userListHTML = "";
            
            data.forEach(function (user) {
                if (user.is_authenticated == 1) {
                    userListHTML += `
                    <li>
                        <div class="user-info">
                            <span class="user-display-name">${user.display_name}</span>
                            <span class="user-username">${user.username}</span>
                            <span class="user-form-group">${user.form_group}</span>
                        </div>
                        <span class="user-status online">Online</span>
                    </li> 
                    `;

                } else {
                    userListHTML += `
                    <li>
                        <div class="user-info">
                            <span class="user-display-name">${user.display_name}</span>
                            <span class="user-username">${user.username}</span>
                            <span class="user-form-group">${user.form_group}</span>
                        </div>
                        <span class="user-status offline">Offline</span>
                    </li> 
                    `;
                }
            });

            userListHTML = `<div class="user-list-container">${userListHTML}</div>`;

            if (document.querySelector('.user-list-container').innerHTML !== userListHTML) {
                document.querySelector('.user-list-container').innerHTML = userListHTML;
            }

        }

    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_group_user_list);
}