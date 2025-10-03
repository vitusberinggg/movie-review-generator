const textBox = document.getElementById("textBox"); // Gets the textbox element
const generateBtn = document.getElementById("generateBtn"); // Gets the button element

function autoExpand(element) {

  /*
  Auto expands given element.

  Arguments:
    "element"
  
  Returns:
    None
  */

  element.style.height = "auto"; // Sets the height to "auto", which shrinks the box if text is deleted
  element.style.height = element.scrollHeight + "px"; // Sets the height to the current scroll height of the element
}

textBox.addEventListener("input", () => autoExpand(textBox)); // Adds event listener to the text box that calls "autoExpand" with argument "textBox" whenever there's input

textBox.addEventListener("keydown", (event) => { // Adds event listener to the textbox that calls following function with argument "event" whenever a key is pressed:
  if (event.key === "Tab") { // If the key pressed is "Tab"
    event.preventDefault(); // Prevent the browsers default behaviour (which is moving focus to the next form field or button)
    generateBtn.click(); // Simulate a click on the button
  }
});

generateBtn.addEventListener("click", async () => { // Adds event listener to the generate button with an asynchronous function:
  
  try { // Try to...
    const response = await fetch("/generate", { // Send a request to the /generate endpoint with following specifications:
      method: "POST", // Use the POST method
      headers: { "Content-Type": "application/json" }, // Set the request header to indicate JSON content
      body: JSON.stringify({text: textBox.value}) // Convert the data to a JSON string and send it in the request body
    });

    if (!response.ok) throw new Error("Server error"); // If the response isn't ok, throw an error

    const data = await response.json(); // Wait for the response, then parse it as JSON and store it in "data"

    if (textBox.value === "") { // If the text box is empty:
    textBox.value = data.result; // Update the result element's text content with the generated result returned from the server

    } else { // Else:
    textBox.value += " " + data.result; // Update it's text content and use a space before
    }
    autoExpand(textBox);
  } catch (err) { // If an error occurs...
    textBox.value = "Error: " + err.message; // Display the error message in the text box
    autoExpand(textBox); // Call "autoExpand" on the text box
  }
});