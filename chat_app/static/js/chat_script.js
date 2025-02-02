const current_url = window.location.href;
const parts = current_url.split('/');
const group_id = parts.pop();

async function scroll_to_bottom() {
    const messages = document.querySelector('.messages');
    messages.scrollTop = messages.scrollHeight;
}

document.addEventListener('DOMContentLoaded', async function () {


    const input = document.querySelector('.send-message input');

    if (input) {
        input.addEventListener('keydown', async function (event) {
            if (event.key === 'Enter') {
                await send_message();
            }
        });
    } else {
        console.error('Input element not found');
    }
    // Call update_message_list once on page load
    //await update_message_list();

    // After update_message_list completes, start latest_group_message loop
    requestAnimationFrame(update_message_list);
    requestAnimationFrame(update_number_online_users);
});

async function send_message() {
    const input = document.querySelector('.send-message input');
    const user_msg = input.value;
    input.value = "";
    /*const messageListHTML = `
                    <div class="message current-user" data-id="null">
                        <div class="message-info">
                            <div class="username">Avinash</div>
                            <div class="datetime">???</div>
                        </div>
                        <div class="text">${user_msg}</div>
                    </div>
                `;

    document.querySelector('.messages').innerHTML += messageListHTML;
    await scroll_to_bottom();*/
    if (user_msg.trim() !== '') {
        try {
            const response = await fetch(`${window.origin}/send-message`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message_content: user_msg,
                    group: group_id
                })
            });


            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status Code: ${response.status}`);
            }



        } catch (error) {
            console.error('Error:', error);
        }

    } else {
        alert("Please enter a message.");
    }
}

async function update_number_online_users() {
    try {
        const response = await fetch(`${window.origin}/number-online-users`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                group_id: group_id
            })
        });

        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        } else {
            
            const data = await response.json();
            console.log(data);
            document.querySelector('.number-online-users').textContent = `Online Users: ${data}`;
        }
    }
    catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_number_online_users);
}

async function update_message_list() {
    try {
        const response = await fetch(`${window.origin}/all-group-messages`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                group_id: group_id
            })
        });

        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        } else {
            const data = await response.json();

            let messageListHTML = "";
            let previousSender = "";
            let previousDateTime = null;

            data.forEach(function (message) {
                let currentDateTime = new Date(message.message_date_time);
                let displayInfo = true;

                if (message.sender_username === previousSender) {
                    if (previousDateTime) {
                        let timeDifference = (currentDateTime - previousDateTime) / (1000 * 60 * 60); // difference in hours
                        if (timeDifference <= 1) {
                            displayInfo = false;
                        }
                    }
                }

                if (displayInfo) {
                    messageListHTML += `
                            <div class="message ${message.usertype}" data-id="${message.message_id}">
                                <div class="message-info">
                                    <div class="username">${message.sender_display_name}</div>
                                    <div class="datetime">${message.message_date_time}</div>
                                </div>
                                <div class="text">${message.message_content}</div>
                            </div>
                        `;
                } else {
                    messageListHTML += `
                            <div class="message ${message.usertype}" data-id="${message.message_id}">
                                <div class="text">${message.message_content}</div>
                            </div>
                        `;
                }

                previousSender = message.sender_username;
                previousDateTime = currentDateTime;
            });

            if (document.querySelector('.messages').innerHTML !== messageListHTML) {
                document.querySelector('.messages').innerHTML = messageListHTML;
                await scroll_to_bottom();
            }
            /*else {
                document.querySelector('.messages').innerHTML = messageListHTML;
            }*/
        }
    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_message_list);
}

//THIS MADE NO NOTICEABLE PERFORMANCE IMPROVEMENT:
/*
async function latest_group_message() {
    try {
        const response = await fetch(`${window.origin}/latest-group-message`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                group_id: group_id
            })
        });

        if (response.status !== 200) {
            throw new Error(`Looks like there was a problem. Status Code: ${response.status}`);
        }
        const data = await response.json();
        //const lastMessageId = document.querySelector('.messages:last-child').dataset.id;
        const lastMessageId = document.querySelector('.messages').lastElementChild.dataset.id;
        //console.log(lastMessageId);
        //console.log(data.message_id);
        //console.log(data.message_id != lastMessageId);
        if (data.message_id != lastMessageId) {
            const messageListHTML = `
                    <div class="message ${data.usertype}" data-id="${data.message_id}">
                        <div class="message-info">
                            <div class="username">${data.sender_display_name}</div>
                            <div class="datetime">${data.message_date_time}</div>
                        </div>
                        <div class="text">${data.message_content}</div>
                    </div>
                `;

            document.querySelector('.messages').innerHTML += messageListHTML;
            await scroll_to_bottom();
        }

    } catch (error) {
        console.error(error);
    }

    //setInterval(latest_group_message, 1000);

}*/