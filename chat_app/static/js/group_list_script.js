async function update_group_list() {
    try {
        const response = await fetch(`${window.origin}/group-list`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
        });

        if (response.status !== 200) {
            console.error(`Looks like there was a problem: ${response.status}`);
        }
        const data = await response.json();
        console.log(`Response ${data}`);
        let groupListHTML = "";
        data.forEach(function (group) {
            console.log(group);
            if (group.any_messages == false) {
                groupListHTML += `
                <a href="${window.origin}/chat/${group.group_id}" id="group_${group.group_id}" class="group">
                    <div class="top-level">
                        <div class="group-name">${group.group_name}</div>
                    </div>
                    <div class="last-message">No messages yet.</div>
                </a>
                `;
            } else {
                let max_length = 30;
                if (group.last_message.length > max_length) {
                    last_message = group.last_message.slice(0, max_length) + '...';
                } else {
                    last_message = group.last_message;
                }
                groupListHTML += `
                <a href="${window.origin}/chat/${group.group_id}" id="group_${group.group_id}" class="group">
                    <div class="top-level">
                        <div class="group-name">${group.group_name}</div>
                        <div class="group-last-message-datetime">${group.last_message_datetime}</div>
                    </div>
                    <div class="last-message">${group.last_message_user_display_name}: ${last_message}</div>
                </a>
                `;
            }
             
        });
        document.querySelector('.chat-groups').innerHTML = groupListHTML;
        
    
    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_group_list);
}

requestAnimationFrame(update_group_list);

