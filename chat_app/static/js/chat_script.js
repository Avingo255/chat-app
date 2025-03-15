async function scroll_to_bottom() {
    // used in update_message_list to scroll to the bottom of the chat messages
    // important
    const messages = document.querySelector('.messages');
    messages.scrollTop = messages.scrollHeight;
}

document.addEventListener('DOMContentLoaded', async function () {
    await update_chat_options_link();

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
                    group: chat_group_id
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



async function update_message_list() {
    try {
        const response = await fetch(`${window.origin}/all-group-messages`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                group_id: chat_group_id
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

// write function to update a link chat-options-link to the groupid in the url ie window.origin/chat/groupid. the chat options link should be in the form window.origin/chat/groupid/options
async function update_chat_options_link() {
    const chatOptionsLink = document.querySelector('.chat-options-link');
    if (chatOptionsLink) {
        chatOptionsLink.href = `${window.origin}/chat/${chat_group_id}/options`;
    } else {
        console.error('Chat options link element not found');
    }
}