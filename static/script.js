let actionList = [];

function addAction(time = '', brightness = '128', index = null) {
    const actionIndex = index !== null ? index : actionList.length;

    const actionContainer = document.createElement('div');
    actionContainer.classList.add('action');

    const timeInput = document.createElement('input');
    timeInput.type = 'time';
    timeInput.value = time;
    timeInput.required = true;

    const brightnessInput = document.createElement('input');
    brightnessInput.type = 'range';
    brightnessInput.min = '0';
    brightnessInput.max = '255';
    brightnessInput.value = brightness;
    brightnessInput.required = true;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function() {
        actionContainer.remove();
        // Remove the action from the actionList array
        actionList = actionList.filter((_, i) => i !== actionIndex);
    };

    actionContainer.appendChild(timeInput);
    actionContainer.appendChild(brightnessInput);
    actionContainer.appendChild(deleteButton);
    document.getElementById('actionList').appendChild(actionContainer);

    // Store a reference to the container for easy deletion
    actionList.push({ timeInput, brightnessInput, deleteButton, container: actionContainer });
}

document.getElementById('submitActions').addEventListener('click', function() {
    const actionsData = actionList.map((action, index) => {
        return {
            time: action.timeInput.value,
            brightness: action.brightnessInput.value,
            index: index  // Include the index to track which action this is
        };
    });

    fetch('/set_schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(actionsData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Actions saved:', data);
    })
    .catch(error => console.error('Error:', error));
});

window.onload = function() {
    const existingActions = JSON.parse('{{ actions | tojson | safe }}').flat();
    existingActions.forEach((action, index) => {
        addAction(action.time, action.brightness, index);
    });
};