function getGroupId(url) {
    const regex = /\/chat\/(\d+)(?:\/options)?/;
    // Regular expression to match the pattern /chat/<int: group id> or /chat/<int: group id>/options
    // - \\/chat\\/ matches the literal string "/chat/"
    // - (\\d+) captures one or more digits (the group id) and stores it in the first capturing group
    // - (?:\\/options)? is a non-capturing group that matches the literal string "/options" if it exists (will also need to work if user is on gruop options page)
        
    const match = url.match(regex);
    if (match) {
        // If a match is found, parse the captured group id as an integer and return it
        return parseInt(match[1], 10);
    }
    return null;
}

const chat_group_id = getGroupId(window.location.pathname);