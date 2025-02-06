document.addEventListener('DOMContentLoaded', async function() {
    const tabs = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', async () => {
            const tabId = tab.getAttribute('data-tab');

            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    requestAnimationFrame(update_received_invite_list);
    requestAnimationFrame(update_outgoing_invite_list);
});

async function scroll_to_top() {
    const invitations = document.querySelector('.invitations');
    invitations.scrollBottom = invitations.scrollHeight;
}

async function accept_invite() {
    // Get the button that triggered the function
    var button = event.target;

    // Get the parent element of the button
    var parent = button.parentElement;

    // Get the parent element of the parent element
    var grandparent = parent.parentElement;

    // Get the data-id attribute of the grandparent element
    var data_id = grandparent.getAttribute('data-id');

    try {
        const response = await fetch(`${window.origin}/accept-invite`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request_id: data_id,
            })
        });
        
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

async function reject_invite() {
    // Get the button that triggered the function
    var button = event.target;

    // Get the parent element of the button
    var parent = button.parentElement;

    // Get the parent element of the parent element
    var grandparent = parent.parentElement;

    // Get the data-id attribute of the grandparent element
    var data_id = grandparent.getAttribute('data-id');

    try {
        const response = await fetch(`${window.origin}/reject-invite`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request_id: data_id,
            })
        });
        
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

async function cancel_outgoing_invite() {
    // Get the button that triggered the function
    var button = event.target;

    // Get the parent element of the button
    var parent = button.parentElement;

    // Get the parent element of the parent element
    var grandparent = parent.parentElement;

    // Get the data-id attribute of the grandparent element
    var data_id = grandparent.getAttribute('data-id');

    try {
        const response = await fetch(`${window.origin}/cancel-outgoing-invite`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request_id: data_id,
            })
        });
        
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

async function update_received_invite_list() {
    try {
        const response = await fetch(`${window.origin}/all-received-group-invites`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
        });
        // no parameters to send in body

        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        } else {
            const data = await response.json();

            let invitationListHTML = "";
            
            data.forEach(function (invite) {
                if (invite.status == "pending") {
                    invitationListHTML += `
                    <div class="invitation pending" data-id="${invite.request_id}">
                        <div class="invite-info">
                            <span class="date">${invite.request_date_time}</span>  
                            <span class="invite-text"><span class="highlight">${invite.sender_username}</span> has invited you to join <span class="highlight">${invite.group_name}</span>!</span>
                        </div>
                        <div class="invite-actions">
                            <button class="accept" onclick="accept_invite(event)">Accept</button>
                            <button class="reject" onclick="reject_invite(event)">Reject</button>
                        </div>
                    </div>  
                    `;

                } else {
                    invitationListHTML += `
                    <div class="invitation past">
                        <div class="invite-info">
                            <span class="date">${invite.request_date_time}</span>  
                            <span class="invite-text">You <span class="highlight">${invite.status}</span> <span class="highlight">${invite.sender_username}</span>'s invitation to join <span class="highlight">${invite.group_name}</span>.</span>
                        </div>
                        <div class="status ${invite.status}">${invite.status.toUpperCase()}</div>
                    </div>
                    `;
                }
            });

            invitationListHTML = `<div class="invitations">${invitationListHTML}</div>`;
            if (data.length == 0) {
                invitationListHTML = `<div class="invitations">
                                        <div class="no-invitations">
                                            <p>No invitations yet.</p>
                                        </div>
                                      </div>
                                      `;
                document.querySelector('#received.tab-content').innerHTML = invitationListHTML;
            } else if (document.querySelector('#received.tab-content').innerHTML !== invitationListHTML) {
                document.querySelector('#received.tab-content').innerHTML = invitationListHTML;
                await scroll_to_top();
            }
        }

    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_received_invite_list);
}

async function update_outgoing_invite_list() {
    try {
        const response = await fetch(`${window.origin}/all-sent-group-invites`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
        });
        // no parameters to send in body

        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status Code: ${response.status}`);
        } else {
            const data = await response.json();

            let invitationListHTML = "";
            
            data.forEach(function (invite) {
                if (invite.status == "pending") {
                    invitationListHTML += `
                    <div class="invitation pending" data-id="${invite.request_id}">
                        <div class="invite-info">
                            <span class="date">${invite.request_date_time}</span>  
                            <span class="invite-text">You invited <span class="highlight">${invite.receiver_username}</span> to join <span class="highlight">${invite.group_name}</span>!</span>
                        </div>
                        <div class="invite-actions">
                            <button class="cancel" onclick="cancel_outgoing_invite()">Cancel</button>
                            <div class="status pending">Pending</div>
                        </div>
                    </div> 
                    `;

                } else {
                    invitationListHTML += `
                    <div class="invitation past">
                        <div class="invite-info">
                            <span class="date">${invite.request_date_time}</span>  
                            <span class="invite-text"><span class="highlight"> ${invite.receiver_username} ${invite.status}</span> your invitation to join <span class="highlight">${invite.group_name}</span>.</span>
                        </div>
                        <div class="status ${invite.status}">${invite.status.toUpperCase()}</div>
                    </div>
                    `;
                }
            });

            invitationListHTML = `<div class="invitations">${invitationListHTML}</div>`;
            if (data.length == 0) {
                invitationListHTML = `<div class="invitations">
                                        <div class="no-invitations">
                                            <p>No invitations yet.</p>
                                        </div>
                                      </div>
                                      `;
                document.querySelector('#outgoing.tab-content').innerHTML = invitationListHTML;
            } else if (document.querySelector('#outgoing.tab-content').innerHTML !== invitationListHTML) {
                document.querySelector('#outgoing.tab-content').innerHTML = invitationListHTML;
                await scroll_to_top();
            } 
            /*else {
                document.querySelector('#outgoing.tab-content').innerHTML = invitationListHTML;
            } */

        }

    } catch (error) {
        console.error(error);
    }
    requestAnimationFrame(update_outgoing_invite_list);
}

