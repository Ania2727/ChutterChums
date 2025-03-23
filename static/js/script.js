console.log("JavaScript Loaded Successfully!");

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".interest-btn");
    
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            if (button.classList.contains("selected")) {
                button.classList.remove("selected");
            } else {
                button.classList.add("selected");
            }
        });
    });

    document.querySelector(".continue-btn").addEventListener("click", function () {
        const selectedInterests = Array.from(document.querySelectorAll(".interest-btn.selected"))
            .map(btn => btn.innerText);
        
        console.log("Selected Interests:", selectedInterests);

        fetch('https://your-aws-api.com/get-recommendations', {
            method: 'POST',
            body: JSON.stringify({ interests: selectedInterests }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Suggested Forums:", data);
            alert("Recommended Forums: " + data.recommendations.join(", "));
        })
        .catch(error => console.error("Error:", error));
    });
});
