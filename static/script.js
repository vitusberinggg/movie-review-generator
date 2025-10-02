const textBox = document.getElementById("textBox");
const generateBtn = document.getElementById("generateBtn");

function autoExpand(el) {
  el.style.height = "auto";
  el.style.height = el.scrollHeight + "px";
}

// Expand on input
textBox.addEventListener("input", () => autoExpand(textBox));


textBox.addEventListener("keydown", (e) => {
  if (e.key === "Tab") {
    e.preventDefault();
    generateBtn.click();
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
    textBox.value = "Error: " + err.message; // Display the error message in the result element
    autoExpand(textBox);
  }
});