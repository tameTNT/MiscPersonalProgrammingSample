let page = document.getElementById('buttonDiv');

let selectedClassName = "current";

var presetButtonColors = Array()

// Populates array with 10 random colours
for (let i = 0; i < 10; i++) {
    let colorString = '#';

    for (let d = 0; d < 6; d++) {  // generates a random colour
        colorString += Math.floor(Math.random() * 16).toString(16); // convert random num (between 0 and 15) to hexadecimal
    };

    presetButtonColors.push(colorString);
}

// Reacts to a button click by marking the selected button and saving the selection
function handleButtonClick(event) {
    // Remove styling from the previously selected color
    let current = event.target.parentElement.querySelector(
        `.${selectedClassName}`
    );
    if (current && current !== event.target) {
        current.classList.remove(selectedClassName);
    }

    // Mark the button as selected
    let color = event.target.dataset.color;
    event.target.classList.add(selectedClassName);
    chrome.storage.sync.set({ color });
}

// Add a button to the page for each supplied color
function constructOptions(buttonColorArray) {
    chrome.storage.sync.get("color", (data) => {
        let currentColor = data.color;
        // For each color we were provided...
        for (let buttonColor of buttonColorArray) {
            // ...create a button with that color
            let button = document.createElement("button");
            button.dataset.color = buttonColor;
            button.style.backgroundColor = buttonColor;

            // ...mark the currently selected color
            if (buttonColor === currentColor) {
                button.classList.add(selectedClassName);
            }

            // ...and register a listener for when that button is clicked
            button.addEventListener("click", handleButtonClick);
            page.appendChild(button);
        }
    });
}

// Initialize the page by constructing the color options
constructOptions(presetButtonColors);