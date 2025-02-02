document.addEventListener('DOMContentLoaded', function() {
    const bubbleBox = document.getElementById('bubbleBox');
    const bubbleInput = document.getElementById('bubbleInput');
    const addBubbleButton = document.getElementById('addBubble');
    const hiddenBubbleList = document.getElementById('hiddenBubbleList');
    const groupNameInput = document.getElementById('group_name');

    function addBubble(value) {
        const bubble = document.createElement('span');
        bubble.className = 'bubble';
        bubble.textContent = value;
        bubble.addEventListener('click', function() {
            bubbleBox.removeChild(bubble);
            updateHiddenField();
        });
        bubbleBox.appendChild(bubble);
        updateHiddenField();
    }

    function updateHiddenField() {
        const bubbles = Array.from(bubbleBox.getElementsByClassName('bubble'));
        hiddenBubbleList.value = bubbles.map(b => b.textContent).join(',');
    }

    function handleAddBubble() {
        const value = bubbleInput.value.trim();
        if (value) {
            addBubble(value);
            bubbleInput.value = '';
        }
    }

    addBubbleButton.addEventListener('click', function(e) {
        e.preventDefault();
        handleAddBubble();
    });

    bubbleInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleAddBubble();
        }
    });

    groupNameInput.addEventListener('input', function() {
        if (this.value.length > 50) {
            this.value = this.value.slice(0, 50);
        }
    });
});