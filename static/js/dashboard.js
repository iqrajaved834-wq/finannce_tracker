
const logout = document.querySelector(".logout-btn");
if (logout) {
    logout.addEventListener("click", async function(event) {
        event.preventDefault();
        try {

            const response = await fetch("/logout", {
                method: "POST"
            });
            const data = await response.json();
            if (response.ok) {
                window.location.href = "/login";
            } else {
                console.log(data.error);
            }
        } catch (error) {

            console.log("Something went wrong.", error);

        }
    });
}

